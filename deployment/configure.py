import json
import os
import pathlib
import socket
import subprocess
import urllib.request

import yaml
from pyinfra import host, inventory  # type: ignore
from pyinfra.facts.server import Hostname, User
from pyinfra.operations import apt, files, python, server, systemd

ROOT_DIR = pathlib.Path(__file__).absolute().parent.parent
CONTROL_PLANE_IP = "10.0.1.1"


# load k3s data
k3s_install_script = ROOT_DIR.joinpath("deployment", "downloaded", "k3s_install.sh")

if not k3s_install_script.exists():
    req = urllib.request.Request(
        "https://get.k3s.io",
        headers={  # default user agent is blocked, pretend to be a browser
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        },
    )
    with urllib.request.urlopen(req) as response:
        with open(k3s_install_script, "wb") as fp:
            fp.write(response.read())

with open(ROOT_DIR.joinpath("deployment", "secrets", "k3s_token"), "r") as fp:
    k3s_token = fp.read().strip()

# setup passwordless sudo
files.block(
    name="Setup passwordless sudo",
    path="/etc/sudoers",
    content=f"{host.get_fact(User)} ALL=(ALL) NOPASSWD: ALL\n",
    _sudo=True,
)

# configure multipath
# https://longhorn.io/kb/troubleshooting-volume-with-multipath/#solution
multipath_config = files.block(
    name="Configure multipath",
    path="/etc/multipath.conf",
    content=pathlib.Path(ROOT_DIR, "deployment", "files", "multipath.conf").read_text(),
    _sudo=True,
)

systemd.service(
    name="Restart multipathd",
    service="multipathd",
    restarted=True,
    _sudo=True,
    _if=multipath_config.did_change,
)

# install packages
# https://longhorn.io/docs/1.7.2/deploy/install/#installing-nfsv4-client
# nfs for longhorn
# network manager for managing network connections
# systemd-resolved for DNS
# htop and nano for debugging
apt.packages(
    name="Install required packages",
    packages=["nfs-common", "network-manager", "systemd-resolved", "htop", "nano"],
    update=True,
    _sudo=True,
)

# disable wifi
if "connectivity=eth" in host.data.get("k8s_labels", []):  # type: ignore
    server.shell(name="Disable wifi", commands="nmcli radio wifi off", _sudo=True)

# adsb prerequisites
# https://github.com/sdr-enthusiasts/docker-readsb-protobuf?tab=readme-ov-file#kernel-module-configuration
if "hardware=adsb" in host.data.get("k8s_labels", []):  # type: ignore
    files.put(
        name="Upload rtlsdr blacklist",
        src=str(ROOT_DIR.joinpath("deployment", "files", "blacklist-rtlsdr.conf")),
        dest="/etc/modprobe.d/blacklist-rtlsdr.conf",
        _sudo=True,
    )

    modules = [
        "rtl2832_sdr",
        "dvb_usb_rtl2832u",
        "dvb_usb_rtl28xxu",
        "dvb_usb_v2",
        "r820t",
        "rtl2830",
        "rtl2832",
        "rtl2838",
        "rtl8192cu",
        "rtl8xxxu",
        "dvb_core",
    ]
    for module in modules:
        server.shell(
            name=f"Unload {module}",
            commands=f"modprobe -r {module}",
            _sudo=True,
        )

    server.shell(
        name="Update boot image",
        commands="update-initramfs -u",
        _sudo=True,
    )

# region Install k3s
# https://docs.k3s.io/datastore/ha-embedded
# https://www.rootisgod.com/2024/Running-an-HA-3-Node-K3S-Cluster/
first_host = inventory.hosts[next(iter(inventory.hosts))]


def update_kubeconfig():
    # replace the server address with the first host
    with open(kube_config, "r") as fp:
        kube_config_data = yaml.safe_load(fp)

    # check if static ip is available
    try:
        host = f"https://{CONTROL_PLANE_IP}:6443"
        json.loads(
            subprocess.check_output(["curl", "-k", host], stderr=subprocess.DEVNULL)
        )
    except Exception:
        # if not, use a host
        host = f"https://{first_host.name}:6443"

    kube_config_data["clusters"][0]["cluster"]["server"] = host

    with open(kube_config, "w") as fp:
        yaml.safe_dump(kube_config_data, fp)


# https://serverfault.com/a/1162813
# adds full hostname to the certificate
base_args = [
    "server",
    "--disable=traefik",
    "--disable=servicelb",
    "--embedded-registry",
    f"--tls-san={host.name}",
    f"--tls-san={CONTROL_PLANE_IP}",
    "--etcd-expose-metrics",
    # https://github.com/Sheldonwl/rpi-cluster-k3s/blob/master/docs/setup-k3s-server.md
    # Increase speed at which pods will be rescheduled if a node goes down
    "--kube-apiserver-arg=default-not-ready-toleration-seconds=20",
    "--kube-apiserver-arg=default-unreachable-toleration-seconds=20",
    "--kube-controller-arg=node-monitor-period=20s",
    "--kube-controller-arg=node-monitor-grace-period=20s",
    "--kubelet-arg=node-status-update-frequency=5s",
]

if first_host.name == host.name:
    server.script(
        name="Run k3s install script on first node",
        src=str(k3s_install_script),
        _env={"K3S_TOKEN": k3s_token},
        args=base_args + ["--cluster-init"],
    )

    # download the kubeconfig file
    kube_config = pathlib.Path(os.path.expanduser("~"), ".kube", "config")
    kube_config.parent.mkdir(exist_ok=True)

    files.get(
        name="Download kubeconfig",
        src="/etc/rancher/k3s/k3s.yaml",
        dest=str(kube_config.absolute()),
        _sudo=True,
    )

    python.call(name="Update kubeconfig", function=update_kubeconfig)

else:
    # resolve first host name to ip address
    first_host_ip = socket.gethostbyname(first_host.name)
    server.script(
        name="Run k3s install script on other nodes",
        src=str(k3s_install_script),
        _env={"K3S_TOKEN": k3s_token},
        args=base_args + [f"--server=https://{first_host_ip}:6443"],
        _serial=True,  # join one at a time
    )

registries_config = files.put(
    name="Upload k3s registry config",
    src=str(ROOT_DIR.joinpath("deployment", "files", "registries.yaml")),
    dest="/etc/rancher/k3s/registries.yaml",
    _sudo=True,
)

k3s_config = files.put(
    name="Upload k3s config",
    src=str(ROOT_DIR.joinpath("deployment", "secrets", "config.yaml")),
    dest="/etc/rancher/k3s/config.yaml",
    _sudo=True,
)

systemd.service(
    name="Restart k3s",
    service="k3s",
    restarted=True,
    _sudo=True,
    # https://docs.pyinfra.com/en/3.x/using-operations.html#operation-changes-output
    _if=lambda: k3s_config.did_change() or registries_config.did_change(),
    # restart k3s one at a time
    _serial=True,
)

# only need to run in one spot on the cluster
for label in host.data.get("k8s_labels", []):  # type: ignore
    server.shell(
        name=f"Label node with {label}",
        commands=f"kubectl label nodes {host.get_fact(Hostname)} {label}",
        _sudo=True,
        _run_once=True,
    )
# endregion

# increase the number of open files
# https://serverfault.com/a/1137212
server.sysctl(
    name="Change the fs.inotify.max_user_watches value",
    key="fs.inotify.max_user_watches",
    value=2099999999,
    persist=True,
    _sudo=True,
)
server.sysctl(
    name="Change the fs.inotify.max_user_instances value",
    key="fs.inotify.max_user_instances",
    value=2099999999,
    persist=True,
    _sudo=True,
)
server.sysctl(
    name="Change the fs.inotify.max_queued_events value",
    key="fs.inotify.max_queued_events",
    value=2099999999,
    persist=True,
    _sudo=True,
)

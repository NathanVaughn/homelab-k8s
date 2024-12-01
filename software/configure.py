import os
import pathlib
import urllib.request

import yaml
from pyinfra import host, inventory  # type: ignore
from pyinfra.facts.server import Hostname
from pyinfra.operations import apt, files, python, server, systemd

ROOT_DIR = pathlib.Path(__file__).absolute().parent.parent

resolvconf_config = "/etc/resolvconf/resolv.conf.d/head"

# load k3s data
k3s_install_script = ROOT_DIR.joinpath("software", "downloaded", "k3s_install.sh")

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

with open(ROOT_DIR.joinpath("software", "secrets", "k3s_token"), "r") as fp:
    k3s_token = fp.read().strip()

# setup passwordless sudo
files.block(
    name="Setup passwordless sudo",
    path="/etc/sudoers",
    content="ubuntu ALL=(ALL) NOPASSWD: ALL\n",
    _sudo=True,
)

# configure multipath
# https://longhorn.io/kb/troubleshooting-volume-with-multipath/#solution
multipath_config = files.block(
    name="Configure multipath",
    path="/etc/multipath.conf",
    content=pathlib.Path(ROOT_DIR, "software", "files", "multipath.conf").read_text(),
    _sudo=True,
)

systemd.service(
    name="Restart multipathd",
    service="multipathd",
    restarted=multipath_config.changed,
    _sudo=True,
)

# disable wifi
if "connectivity=eth" in host.data.get("k8s_labels", []):  # type: ignore
    apt.packages(
        name="Install NetworkManager",
        packages=["network-manager"],
        update=True,
        _sudo=True,
    )
    server.shell(name="Disable wifi", commands="nmcli radio wifi off", _sudo=True)

# region Install k3s
# https://docs.k3s.io/datastore/ha-embedded
# https://www.rootisgod.com/2024/Running-an-HA-3-Node-K3S-Cluster/
first_host = inventory.hosts[next(iter(inventory.hosts))]


def update_kubeconfig():
    # replace the server address with the first host
    with open(kube_config, "r") as fp:
        kube_config_data = yaml.safe_load(fp)

    kube_config_data["clusters"][0]["cluster"]["server"] = "https://10.0.1.1:6443"

    # may need this on first run until kube-vip is up
    # kube_config_data["clusters"][0]["cluster"]["server"] = (
    #     f"https://{first_host.name}:6443"
    # )

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
    "--tls-san=10.0.1.1",
]

if first_host.name == host.name:
    server.script(
        name="Run k3s install script on first node",
        src=k3s_install_script,
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
    server.script(
        name="Run k3s install script on other nodes",
        src=k3s_install_script,
        _env={"K3S_TOKEN": k3s_token},
        args=base_args + [f"--server=https://{first_host.name}:6443"],
    )

files.put(
    name="Upload k3s registry config",
    src=ROOT_DIR.joinpath("software", "files", "registries.yaml"),
    dest="/etc/rancher/k3s/registries.yaml",
    _sudo=True,
)

files.put(
    name="Upload k3s config",
    src=ROOT_DIR.joinpath("software", "secrets", "config.yaml"),
    dest="/etc/rancher/k3s/config.yaml",
    _sudo=True,
)

for label in host.data.get("k8s_labels", []):  # type: ignore
    server.shell(
        name=f"Label node with {label}",
        commands=f"kubectl label nodes {host.get_fact(Hostname)} {label}",
        _sudo=True,
    )
# endregion


# TODO only do this for the DNS server
if False:
    apt.packages(
        name="Install resolvconf",
        packages=["resolvconf"],
        update=True,
        _sudo=True,
    )

    resolvconf_config_edit = files.block(
        name="Edit resolvconf configuration",
        path=resolvconf_config,
        content="nameserver 1.1.1.1\nnameserver 1.0.0.1\n",  # last newline is important
    )

    server.service(
        name="Start resolvconf",
        service="resolvconf",
        runing=True,
        restarted=resolvconf_config_edit.changed,
    )

    if resolvconf_config_edit.changed:
        server.shell(name="Update /etc/resolv.conf", commands="resolvconf -u")

        server.service(
            name="Start systemd-resolved",
            service="systemd-resolved",
            runing=True,
            restarted=resolvconf_config_edit.changed,
        )

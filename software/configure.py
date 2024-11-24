import pathlib
import urllib.request

from pyinfra import host, inventory  # type: ignore
from pyinfra.operations import apt, files, server

ROOT_DIR = pathlib.Path(__file__).absolute().parent.parent

resolvconf_config = "/etc/resolvconf/resolv.conf.d/head"

# load k3s data
k3s_install_script = ROOT_DIR.joinpath("downloaded", "k3s_install.sh")

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

# region setup passwordless sudo
files.block(
    name="Setup passwordless sudo",
    path="/etc/sudoers",
    content="ubuntu ALL=(ALL) NOPASSWD: ALL\n",
    _sudo=True,
)
# endregion

# region disable wifi
apt.packages(
    name="Install NetworkManager",
    packages=["network-manager"],
    update=True,
    _sudo=True,
)
server.shell(name="Disable wifi", commands="nmcli radio wifi off", _sudo=True)
# endregion

# region Install k3s
# https://docs.k3s.io/datastore/ha-embedded
# https://www.rootisgod.com/2024/Running-an-HA-3-Node-K3S-Cluster/
first_host = inventory.hosts[next(iter(inventory.hosts))]

if first_host.name == host.name:
    server.script(
        name="Run k3s install script on first node",
        src=k3s_install_script,
        _env={"K3S_TOKEN": k3s_token},
        # https://serverfault.com/a/1162813
        # adds full hostname to the certificate
        args=("server", "--cluster-init", f"--tls-san={first_host.name}"),
    )

else:
    server.script(
        name="Run k3s install script on other nodes",
        src=k3s_install_script,
        _env={"K3S_TOKEN": k3s_token},
        args=(
            "server",
            f"--server=https://{first_host.name}:6443",
            f"--tls-san={host.name}",
        ),
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

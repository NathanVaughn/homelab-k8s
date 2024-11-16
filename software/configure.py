from pyinfra.operations import apt, files, server

temp_k3s_file = "/tmp/install_k3s.sh"
resolvconf_config = "/etc/resolvconf/resolv.conf.d/head"

# region Install k3s
files.download(
    name="Donwload k3s install script",
    src="https://get.k3s.io",
    dest=temp_k3s_file,
)

files.file(name="Make k3s install script executable", path=temp_k3s_file, mode="+x")

server.shell(name="Run k3s install script", commands=temp_k3s_file)

files.file(name="Delete k3s install script", path=temp_k3s_file, present=False)
# endregion


# TODO only do this for the DNS server
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

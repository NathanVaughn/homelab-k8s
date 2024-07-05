from pyinfra.operations import files, server, apt

temp_k3s_file = "/tmp/install_k3s.sh"
smartd_dir = "/var/log/smartd"
smartd_config = "/etc/default/smartmontools"
smartd_logrotate = "/etc/logrotate.d/smartd"
resolvconf_config = "/etc/resolvconf/resolv.conf.d/head"

# region Install lm-sensors
apt.packages(
    name="Install lm-sensors",
    packages=["lm-sensors"],
    update=True,
    _sudo=True,
)
# endregion

# region Install smartmontools
# https://learn.netdata.cloud/docs/collecting-metrics/hardware-devices-and-sensors/s.m.a.r.t.#configure-smartd-to-write-attribute-information-to-files
apt.packages(
    name="Install smartmontools",
    packages=["smartmontools"],
    update=True,
    _sudo=True,
)

files.block(
    name="Edit smartd configuration file",
    path=smartd_config,
    content=f'smartd_opts="-A {smartd_dir} -i 600',
)

files.directory(name="Create smartd log directory", path=smartd_dir, present=True)

apt.packages(
    name="Install logrotate",
    packages=["logrotate"],
    update=True,
    _sudo=True,
)

files.block(
    name="Edit smartd logrotate configuration",
    path=smartd_logrotate,
    content="/var/log/smartd/* {\n\tweekly\n\tmaxsize 10M\n}",
)

server.service(name="Start smartd", service="smatd", running=True, enabled=True)
# endregion

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

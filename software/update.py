from pyinfra import host  # type: ignore
from pyinfra.facts import files as files_facts
from pyinfra.facts import server as server_facts
from pyinfra.operations import apt, python, server

apt.update(name="Update apt cache", _sudo=True)
apt.dist_upgrade(name="apt dist-upgrade", _sudo=True)
apt.upgrade(name="apt upgrade --autoremove", auto_remove=True, _sudo=True)


def reboot_node():
    # first install netstat, since we need it after it reboots
    apt.packages(
        name="Install net-tools",
        packages=["net-tools"],
        _sudo=True,
    )

    # cordon the node
    server.shell(
        name="Cordon the node",
        commands=f"kubectl cordon {host.get_fact(server_facts.Hostname)}",
        _sudo=True,
    )

    # drain the node
    server.shell(
        name="Drain the node",
        # without --disable-eviction, longhorn may make it wait forever.
        # ---
        # try without `--disable-eviction`, as this gives Longhorn
        # time to replicate the volume before rebooting
        commands=f"kubectl drain --delete-emptydir-data --ignore-daemonsets {host.get_fact(server_facts.Hostname)}",
        _sudo=True,
    )

    # reboot
    server.reboot(name="Reboot the server", interval=5, _sudo=True)

    # wait for the kubernetes server to come back
    # this uses netstat
    server.wait(
        name="Wait for k3s to start",
        port=6443,
    )

    # uncordon the node
    max_retries = 10
    for attempt in range(1, max_retries + 1):
        result = server.shell(
            name="Uncordon the node",
            commands=f"kubectl uncordon {host.get_fact(server_facts.Hostname)}",
            _sudo=True,
        )

        if result.did_succeed():
            break

        server.shell(
            name="Retry wait",
            commands=f"sleep {attempt * 2}",
        )


# check if server needs a reboot
# https://docs.pyinfra.com/en/3.x/facts/files.html#files-file
if host.get_fact(files_facts.File, "/var/run/reboot-required"):
    python.call(name="Reboot the server", function=reboot_node, _serial=True)

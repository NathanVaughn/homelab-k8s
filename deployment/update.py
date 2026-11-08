import shlex
import subprocess
import time

from pyinfra import host, inventory
from pyinfra.api import Host
from pyinfra.facts import server as server_facts
from pyinfra.operations import apt, python, server

apt.update(name="Update apt cache", _sudo=True)
apt.dist_upgrade(name="apt dist-upgrade", _sudo=True)
apt.upgrade(name="apt upgrade --autoremove", auto_remove=True, _sudo=True)


def run_kubectl_on_control_plane(
    control_plane: Host, arguments: list[str], ignore_errors: bool = False
) -> bool:
    node_name = control_plane.get_fact(server_facts.Hostname)
    node_ip = subprocess.check_output(
        [
            "kubectl",
            "get",
            "node",
            node_name,
            "-o",
            'jsonpath={.status.addresses[?(@.type=="InternalIP")].address}',
        ],
        text=True,
    ).strip()
    if not node_ip:
        raise RuntimeError(f"No InternalIP found for control-plane node {node_name}")

    ssh_command = [
        "ssh",
        "-o",
        f"HostName={node_ip}",
        "-o",
        f"HostKeyAlias={control_plane.name}",
        "-o",
        "BatchMode=yes",
        "-o",
        "ConnectTimeout=5",
        f"{control_plane.data.get('ssh_user', 'ubuntu')}@{control_plane.name}",
        f"sudo kubectl {shlex.join(arguments)}",
    ]
    result = subprocess.run(ssh_command, check=False)
    if result.returncode and not ignore_errors:
        raise subprocess.CalledProcessError(result.returncode, ssh_command)
    return result.returncode == 0


def reboot_node() -> None:
    node_name = host.get_fact(server_facts.Hostname)
    control_plane = next(
        candidate
        for candidate in inventory.hosts.values()
        if candidate.name != host.name and candidate.data.get("etcd_voter", True)
    )

    # cordon the node
    run_kubectl_on_control_plane(control_plane, ["cordon", node_name])

    # drain the node
    # without --disable-eviction, longhorn may make it wait forever.
    # ---
    # try without `--disable-eviction`, as this gives Longhorn
    # time to replicate the volume before rebooting
    run_kubectl_on_control_plane(
        control_plane,
        [
            "drain",
            "--delete-emptydir-data",
            "--v=2",
            "--ignore-daemonsets",
            node_name,
        ],
    )

    # reboot
    server.reboot(name="Reboot the server", interval=5, reboot_timeout=600, _sudo=True)

    run_kubectl_on_control_plane(
        control_plane,
        [
            "wait",
            "--for=condition=Ready",
            f"node/{node_name}",
            "--timeout=600s",
        ],
    )

    # uncordon the node
    max_retries = 10
    for attempt in range(1, max_retries + 1):
        if run_kubectl_on_control_plane(
            control_plane, ["uncordon", node_name], ignore_errors=True
        ):
            break

        time.sleep(attempt * 2)
    else:
        raise RuntimeError(
            f"Failed to uncordon node {node_name} after {max_retries} attempts"
        )


# check if server needs a reboot
result = server.shell(
    name="Check if server needs a reboot",
    commands="test -f /var/run/reboot-required",
    _ignore_errors=True,
)
python.call(
    name="Reboot the server",
    function=reboot_node,
    _serial=True,
    _if=result.did_succeed,
)

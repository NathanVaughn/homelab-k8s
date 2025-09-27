from pyinfra.operations import python, server, systemd


def delete_pod() -> None:
    pod_name = server.shell(
        name="Get chrony pod name",
        commands="kubectl get pods -n chrony -o jsonpath='{.items[0].metadata.name}'",
        _sudo=True,
    )

    server.shell(
        name="Delete chrony pod to force restart",
        commands=f"kubectl delete pod {pod_name.stdout} -n chrony",
        _sudo=True,
    )

    # Wait for chrony pod to be running
    # This is a simple wait, not a check
    server.shell(
        name="Wait for chrony pod to be running",
        commands="sleep 5",
    )


python.call(
    name="Delete chrony pod and wait for restart",
    function=delete_pod,
    _run_once=True,
)

# restart time sync on all nodes
systemd.service(
    name="Restart systemd-timesyncd",
    service="systemd-timesyncd",
    restarted=True,
    _sudo=True,
)

import subprocess


def restart_daemonset(namespace: str, daemonset_name: str) -> None:
    """
    Restart a specific DaemonSet in a given namespace.
    """

    print(f"Restarting DaemonSet '{daemonset_name}' in namespace '{namespace}'")
    subprocess.run(
        [
            "kubectl",
            "rollout",
            "restart",
            "daemonset",
            daemonset_name,
            "-n",
            namespace,
        ],
        check=True,
    )


def get_all_daemonsets() -> list[tuple[str, str]]:
    """
    Get a list of all DaemonSets in all namespaces.
    Returns a list of tuples (namespace, daemonset_name).
    """

    result = subprocess.run(
        [
            "kubectl",
            "get",
            "daemonsets",
            "--all-namespaces",
            "-o",
            "custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name",
            "--no-headers",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    daemonsets = []
    for line in result.stdout.strip().split("\n"):
        namespace, name = line.split()
        daemonsets.append((namespace, name))

    return daemonsets


if __name__ == "__main__":
    daemonsets = get_all_daemonsets()
    for namespace, daemonset_name in daemonsets:
        restart_daemonset(namespace, daemonset_name)

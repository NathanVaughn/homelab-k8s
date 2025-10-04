import argparse
import pathlib
import subprocess
from typing import Literal

THIS_DIR = pathlib.Path(__file__).parent
BASE_DIR = THIS_DIR.parent
CLUSTER_DIR = BASE_DIR.joinpath("cluster")


def kubectl_exec(namespace: str, container: str, command: list[str]) -> str:
    cmd = ["kubectl", "exec", "-n", namespace, container, "--"] + command
    print("> " + " ".join(cmd))
    return subprocess.run(
        cmd,
        text=True,
        capture_output=True,
    ).stdout


def find_postgres_namespaces() -> list[str]:
    """
    Return a list of namespaces that have PostgreSQL deployments.
    """
    namespaces = []
    for filename in CLUSTER_DIR.glob("**/deployment-postgresql.yaml"):
        namespace = filename.parent.name
        namespaces.append(namespace)

    return namespaces


def find_container(namespace: str) -> str:
    """
    Return the name of the PostgreSQL container running in the given namespace.
    """
    names = subprocess.run(
        [
            "kubectl",
            "get",
            "pods",
            "-n",
            namespace,
            "-o",
            "jsonpath={.items[*].metadata.name}",
        ],
        capture_output=True,
        text=True,
    ).stdout.split()

    return next(name for name in names if "postgresql" in name or "postgres" in name)


def create_backup(namespace: str, container: str) -> None:
    """
    Create a backup of the PostgreSQL database in the given namespace and container.
    """
    with open(THIS_DIR.joinpath("postgres", f"{namespace}.sql"), "w") as fp:
        fp.write(
            kubectl_exec(
                namespace,
                container,
                [
                    "sh",
                    "-c",
                    # user and database should be same as namespace
                    f"pg_dump -U {namespace} {namespace}",
                ],
            )
        )


def wipe_data(namespace: str, container: str) -> None:
    """
    Wipe the existing directory to allow for an upgrade
    """
    if (
        input("Are you sure you want to delete the data directory? (y/n) ").lower()
        == "y"
    ):
        kubectl_exec(
            namespace,
            container,
            [
                "rm",
                "-rf",
                "/var/lib/postgresql/data/pgdata",
            ],
        )


def restore_backup(namespace: str, container: str) -> None:
    """
    Restore the backup of the PostgreSQL database in the given namespace and container.
    """

    subprocess.run(
        [
            "kubectl",
            "cp",
            THIS_DIR.joinpath("postgres", f"{namespace}.sql"),
            f"{namespace}/{container}:/tmp/{namespace}.sql",
        ],
        check=True,
    )

    kubectl_exec(
        namespace,
        container,
        [
            "sh",
            "-c",
            # user and database should be same as namespace
            f"psql -U {namespace} -h localhost -f /tmp/{namespace}.sql",
        ],
    )
    kubectl_exec(
        namespace,
        container,
        [
            "sh",
            "-c",
            f"psql -U {namespace} -h localhost -c 'ALTER DATABASE {namespace} REFRESH COLLATION VERSION;'",
        ],
    )


def main(namespace: str | None, action: Literal["backup", "wipe", "restore"]) -> None:
    # Determine namespaces to operate on
    if namespace:
        namespaces = [namespace]
    else:
        namespaces = find_postgres_namespaces()

    for namespace in namespaces:
        container = find_container(namespace)

        if action == "backup":
            print(f"Creating backup for namespace: {namespace}, container: {container}")
            create_backup(namespace, container)
        elif action == "wipe":
            print(
                f"Wiping data directory for namespace: {namespace}, container: {container}"
            )
            wipe_data(namespace, container)
        elif action == "restore":
            print(
                f"Restoring backup for namespace: {namespace}, container: {container}"
            )
            restore_backup(namespace, container)
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Help backup and upgrade Postgres DBs")
    parser.add_argument(
        "--namespace",
        default=None,
        type=str,
        help="Specific namespace to backup. Defaults to all",
    )
    parser.add_argument(
        "action",
        type=str,
        choices=["backup", "wipe", "restore"],
        help="Action to perform",
    )
    args = parser.parse_args()

    main(namespace=args.namespace, action=args.action)

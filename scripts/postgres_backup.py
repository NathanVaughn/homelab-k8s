import argparse
import pathlib
import subprocess
from typing import Literal

THIS_DIR = pathlib.Path(__file__).parent.parent
CLUSTER_DIR = THIS_DIR.joinpath("cluster")


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
    subprocess.run(
        [
            "kubectl",
            "exec",
            "-n",
            namespace,
            container,
            "--",
            "sh",
            "-c",
            # user and database should be same as namespace
            f"pg_dump -U {namespace} {namespace} > /var/lib/postgresql/data/backup.sql",
        ]
    )


def rename_data(namespace: str, container: str) -> None:
    """
    Rename the existing directory to allow for an upgrade
    """
    subprocess.run(
        [
            "kubectl",
            "exec",
            "-n",
            namespace,
            container,
            "--",
            "mv",
            "/var/lib/postgresql/data/pgdata",
            "/var/lib/postgresql/data/pgdata-old",
        ]
    )


def restore_backup(namespace: str, container: str) -> None:
    """
    Restore the backup of the PostgreSQL database in the given namespace and container.
    """
    subprocess.run(
        [
            "kubectl",
            "exec",
            "-n",
            namespace,
            container,
            "--",
            "sh",
            "-c",
            # user and database should be same as namespace
            f"psql -U {namespace} -h localhost -f /var/lib/postgresql/data/backup.sql",
        ]
    )
    subprocess.run(
        [
            "kubectl",
            "exec",
            "-n",
            namespace,
            container,
            "--",
            "sh",
            "-c",
            f"psql -U {namespace} -h localhost -c 'ALTER DATABASE {namespace} REFRESH COLLATION VERSION;'",
        ]
    )


def main(namespace: str | None, action: Literal["backup", "rename", "restore"]) -> None:
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
        elif action == "rename":
            print(
                f"Renaming data directory for namespace: {namespace}, container: {container}"
            )
            rename_data(namespace, container)
        elif action == "restore":
            print(
                f"Restoring backup for namespace: {namespace}, container: {container}"
            )
            restore_backup(namespace, container)


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
        choices=["backup", "rename", "restore"],
        help="Action to perform",
    )
    args = parser.parse_args()

    main(namespace=args.namespace, action=args.action)

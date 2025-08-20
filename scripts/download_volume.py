import sys

import fabric

sys.path.append(".")

from scripts import common


def main(namespace: str, name: str):
    node_hostname, mount_path = common.find_volume(namespace, name)

    # ssh into node
    connection = fabric.Connection(node_hostname, user="ubuntu")

    # create archive
    tar_file_base = f"{name}.tar"
    remote_tar_file = f"/tmp/{tar_file_base}"
    local_tar_file = f"tar/{tar_file_base}"
    print(f"Creating archive from {mount_path}")
    connection.run(
        f"sudo tar --create --verbose --file {remote_tar_file} --directory {mount_path} --exclude='lost+found' .",
        hide=False,
    )

    # download it
    print("Downloading archive")
    connection.get(remote=remote_tar_file, local=local_tar_file)

    # delete it
    connection.run(f"sudo rm {remote_tar_file}", hide=True)
    print("Done.")


if __name__ == "__main__":
    namespace = input("Enter the PersistentVolumeClaim namespace: ").strip()
    name = input("Enter the PersistentVolumeClaim name: ").strip()

    main(namespace=namespace, name=name)

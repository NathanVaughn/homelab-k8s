import common
import fabric


def main(namespace: str, name: str):
    node_hostname, mount_path = common.find_volume(namespace, name)

    # ssh into node
    connection = fabric.Connection(node_hostname, user="ubuntu")

    # upload it
    tar_file_base = f"{name}.tar"
    remote_tar_file = f"/tmp/{tar_file_base}"
    local_tar_file = f"tar/{tar_file_base}"
    print("Uploading archive")
    connection.put(local=local_tar_file, remote=remote_tar_file)

    # wipe existing directory
    print(f"Deleting existing content at {mount_path}")
    connection.run(
        f"sudo rm -rf {mount_path}/*",
        hide=True,
    )

    # create archive
    print("Extracting archive")
    connection.run(
        f"sudo tar --extract --verbose --file {remote_tar_file} --directory {mount_path}",
        hide=False,
    )

    # delete it
    connection.run(f"sudo rm {remote_tar_file}", hide=True)
    print("Done.")


if __name__ == "__main__":
    print("!!! Warning: This will overwrite all existing data !!! ")
    namespace = input("Enter the PersistentVolumeClaim namespace: ").strip()
    name = input("Enter the PersistentVolumeClaim name: ").strip()

    main(namespace=namespace, name=name)

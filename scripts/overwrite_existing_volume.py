import json
import subprocess

import fabric


def make_list_of_pvc_names(pod_info: dict) -> list[str]:
    spec = pod_info["spec"]
    if "volumes" not in spec:
        return []

    names = []
    for vol in spec["volumes"]:
        if "persistentVolumeClaim" in vol:
            names.append(vol["persistentVolumeClaim"]["claimName"])

    return names


def main(namespace: str, name: str):
    # look at pvc, find volume id
    pvc_data = json.loads(
        subprocess.check_output(
            ["kubectl", "get", "pvc", "-o", "json", "-n", namespace, name]
        )
    )
    volume_id = pvc_data["spec"]["volumeName"]

    # figure out which node the volume is attached to
    all_pods = json.loads(
        subprocess.check_output(
            ["kubectl", "get", "pods", "-o", "json", "-n", namespace]
        )
    )
    pod_info = next(
        p
        for p in all_pods["items"]
        if name
        # make a list of pvc names attached to the pod
        in make_list_of_pvc_names(p)
    )
    node_hostname = f"{pod_info['spec']['nodeName']}.nathanv.home"
    pod_id = pod_info["metadata"]["uid"]
    print(f"Found volume {volume_id} on node {node_hostname}")

    mount_path = (
        f"/var/lib/kubelet/pods/{pod_id}/volumes/kubernetes.io~csi/{volume_id}/mount"
    )

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
        hide=True,
    )

    # delete it
    connection.run(f"sudo rm {remote_tar_file}", hide=True)
    print("Done.")


if __name__ == "__main__":
    namespace = input("Enter the PersistentVolumeClaim namespace: ").strip()
    name = input("Enter the PersistentVolumeClaim name: ").strip()

    main(namespace=namespace, name=name)

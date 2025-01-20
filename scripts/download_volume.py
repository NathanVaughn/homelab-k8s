import json
import subprocess

import fabric


def main(namespace: str, name: str):
    # look at pvc, find volume name
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
        in [n["persistentVolumeClaim"]["claimName"] for n in p["spec"]["volumes"]]
    )
    node_hostname = f"{pod_info['spec']['nodeName']}.nathanv.home"
    pod_id = pod_info["metadata"]["uid"]
    print(f"Found volume {volume_id} on node {node_hostname}")

    mount_path = (
        f"/var/lib/kubelet/pods/{pod_id}/volumes/kubernetes.io~csi/{volume_id}/mount"
    )

    # ssh into node
    connection = fabric.Connection(node_hostname, user="ubuntu")

    # create archive
    tar_file_base = f"{name}.tar"
    remote_tar_file = f"/tmp/{tar_file_base}"
    local_tar_file = f"tar/{tar_file_base}"
    print(f"Creating archive from {mount_path}")
    connection.run(
        f"sudo tar --create --verbose --file {remote_tar_file} --directory {mount_path} --exclude='lost+found' .",
        hide=True,
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

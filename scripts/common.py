import json
import os
import subprocess

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))


def make_list_of_pvc_names(pod_info: dict) -> list[str]:
    """
    Builds a list of persistent volume claim names for a pods
    """
    spec = pod_info["spec"]
    if "volumes" not in spec:
        return []

    names = []
    for vol in spec["volumes"]:
        if "persistentVolumeClaim" in vol:
            names.append(vol["persistentVolumeClaim"]["claimName"])

    return names


def find_volume(namespace: str, name: str) -> tuple[str, str]:
    """
    Finds what node and path a volume resides at.
    """
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

    return node_hostname, mount_path

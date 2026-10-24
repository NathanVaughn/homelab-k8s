app_servers = [
    # order here is somewhat important. The first node listed will be used
    # to bootstrap the cluster. Ensure it is a node that makes sense
    # (one of the ThinkCenter boxes) and that it is an etcd voter.
    # etcd_voter=True nodes run k3s servers (control plane + etcd, keep this at 3 or 5),
    # etcd_voter=False nodes run k3s agents.
    (
        "billy.nathanv.home",
        {
            "ssh_user": "ubuntu",
            "etcd_voter": True,
            "k8s_labels": ["role=apps", "connectivity=eth"],
        },
    ),
    (
        "jesse.nathanv.home",
        {
            "ssh_user": "ubuntu",
            "etcd_voter": True,
            "k8s_labels": ["role=apps", "connectivity=eth"],
        },
    ),
    (
        "tom.nathanv.home",
        {
            "ssh_user": "ubuntu",
            "etcd_voter": True,
            "k8s_labels": ["role=apps", "connectivity=eth"],
        },
    ),
    (
        "annie.nathanv.home",
        {
            "ssh_user": "ubuntu",
            "etcd_voter": True,
            "k8s_labels": ["role=apps", "connectivity=eth"],
        },
    ),
    (
        "will.nathanv.home",
        {
            "ssh_user": "ubuntu",
            "etcd_voter": True,
            "k8s_labels": ["role=apps", "connectivity=eth", "hardware=adsb"],
        },
    ),
    (
        "cassidy.nathanv.home",
        {
            "ssh_user": "ubuntu",
            "etcd_voter": False,
            "k8s_labels": ["role=3dprint", "connectivity=wifi", "hardware=3dprinter"],
        },
    ),
    (
        "butch.nathanv.home",
        {
            "ssh_user": "ubuntu",
            "etcd_voter": False,
            "k8s_labels": ["role=network", "connectivity=eth"],
        },
    ),
]

# Labels:
# hardware=adsb
# hardware=3dprinter
# role=apps
# role=network
# role=3dprint
# connectivity=wifi
# connectivity=eth

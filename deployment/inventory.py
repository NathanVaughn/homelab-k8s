app_servers = [
    # order here is somewhat important. The first node listed will be used
    # to bootstrap the cluster. Ensure it is a node that makes sense
    # (one of the ThinkCenter boxes)
    (
        "billy.nathanv.home",
        {"ssh_user": "ubuntu", "k8s_labels": ["role=apps", "connectivity=eth"]},
    ),
    (
        "jesse.nathanv.home",
        {"ssh_user": "ubuntu", "k8s_labels": ["role=apps", "connectivity=eth"]},
    ),
    (
        "tom.nathanv.home",
        {"ssh_user": "ubuntu", "k8s_labels": ["role=apps", "connectivity=eth"]},
    ),
    (
        "annie.nathanv.home",
        {"ssh_user": "ubuntu", "k8s_labels": ["role=apps", "connectivity=eth"]},
    ),
    (
        "will.nathanv.home",
        {
            "ssh_user": "ubuntu",
            "k8s_labels": ["role=apps", "connectivity=eth", "hardware=adsb"],
        },
    ),
    (
        "cassidy.nathanv.home",
        {
            "ssh_user": "ubuntu",
            "k8s_labels": ["role=3dprint", "connectivity=wifi", "hardware=3dprinter"],
        },
    ),
    (
        "butch.nathanv.home",
        {"ssh_user": "ubuntu", "k8s_labels": ["role=network", "connectivity=eth"]},
    ),
]

# Labels:
# hardware=adsb
# hardware=ups
# hardware=3dprinter
# role=apps
# role=network
# role=3dprint
# role=games
# connectivity=wifi
# connectivity=eth

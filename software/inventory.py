app_servers = [
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
]

# We don't want to schedule jobs on the 3d print server
# as that's on wifi

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

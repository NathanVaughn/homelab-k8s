app_servers = [
    ("billy.nathanv.home", {"ssh_user": "ubuntu"}),
    ("jesse.nathanv.home", {"ssh_user": "ubuntu"}),
    ("tom.nathanv.home", {"ssh_user": "ubuntu"}),
    ("annie.nathanv.home", {"ssh_user": "ubuntu"}),
    (
        "will.nathanv.home",
        {
            "ssh_user": "ubuntu",
            "k8s_labels": ["role=apps", "connectivity=eth", "hardware=adsb"],
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

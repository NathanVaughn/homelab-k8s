_base_zone = ".nathanv.home"

_app_server_names = ["billy", "jesse", "tom", "annie"]
app_servers = [
    (f"{name}{_base_zone}", {"ssh_user": "ubuntu"}) for name in _app_server_names
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

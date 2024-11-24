_base_zone = ".nathanv.home"
_names = ["billy", "jesse", "tom", "annie"]

nodes = [(f"{name}{_base_zone}", {"ssh_user": "ubuntu"}) for name in _names]

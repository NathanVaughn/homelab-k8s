import argparse
import os
import urllib.request

import yaml
from passlib.handlers.sha2_crypt import sha512_crypt

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILE = os.path.join(THIS_DIR, "autoinstall.tmpl.yaml")
OUTPUT_FILE = os.path.join(THIS_DIR, "autoinstall.yaml")


def main(hostname: str, password: str, ssid_name: str, ssid_password: str) -> None:
    with open(TEMPLATE_FILE) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    # Download the SSH public key
    ssh_key_url = (
        "https://raw.githubusercontent.com/NathanVaughn/public-keys/main/ssh.pub"
    )
    with urllib.request.urlopen(ssh_key_url) as response:
        ssh_key = response.read().decode("utf-8").strip()

    data["autoinstall"]["identity"]["hostname"] = hostname
    data["autoinstall"]["identity"]["password"] = sha512_crypt.using(rounds=5000).hash(
        password
    )

    data["autoinstall"]["ssh"]["authorized-keys"] = [ssh_key]

    # add Wifi credentials and package
    if ssid_name and ssid_password:
        data["autoinstall"]["network"]["wifis"]["wlp2s0"]["access-points"] = {
            ssid_name: {"password": ssid_password}
        }
        data["autoinstall"]["packages"].append("wpasupplicant")
    else:
        del data["autoinstall"]["network"]["wifis"]

    with open(OUTPUT_FILE, "w") as f:
        yaml.dump(data, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", type=str, help="The hostname of the machine.")
    parser.add_argument("password", type=str, help="The password of the machine.")

    parser.add_argument("--ssid-name", type=str, help="The SSID name.")
    parser.add_argument("--ssid-password", type=str, help="The SSID password.")

    args = parser.parse_args()

    main(args.hostname, args.password, args.ssid_name, args.ssid_password)

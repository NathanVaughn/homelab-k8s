import yaml
import os
import argparse
import urllib.request
import subprocess

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILE = os.path.join(THIS_DIR, "autoinstall.tmpl.yaml")
OUTPUT_FILE = os.path.join(THIS_DIR, "autoinstall.yaml")


def main(hostname: str, password: str) -> None:
    with open(TEMPLATE_FILE, "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    # Download the SSH public key
    ssh_key_url = (
        "https://raw.githubusercontent.com/NathanVaughn/public-keys/main/ssh.pub"
    )
    with urllib.request.urlopen(ssh_key_url) as response:
        ssh_key = response.read().decode("utf-8").strip()

    data["autoinstall"]["identity"]["hostname"] = hostname
    data["autoinstall"]["identity"]["password"] = subprocess.check_output(
        ["mkpasswd", "-m", "sha-512", password]
    ).decode("utf-8").strip()

    data["autoinstall"]["ssh"]["authorized-keys"] = [ssh_key]

    with open(OUTPUT_FILE, "w") as f:
        yaml.dump(data, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", type=str, help="The hostname of the machine.")
    parser.add_argument("password", type=str, help="The password of the machine.")
    args = parser.parse_args()

    main(args.hostname, args.password)

import json
import subprocess

# Run this script to create a config to paste into the configmap.


def main():
    dns_configs = json.loads(
        subprocess.check_output(
            [
                "kubectl",
                "get",
                "dnsconfigs.nathanv.me",
                "--all-namespaces",
                "-o",
                "json",
            ]
        )
    )

    with open("config.yaml", "w") as fp:
        fp.write("tunnel: k8s-tunnel\n")
        fp.write("credentials-file: /etc/cloudflared/creds/credentials.json\n")
        fp.write("metrics: 0.0.0.0:2000\n")
        fp.write("no-autoupdate: true\n")
        fp.write("ingress:\n")

        for dns_config in dns_configs["items"]:
            if dns_config["spec"].get("externalCNAME"):
                fp.write(f"- hostname: {dns_config['spec'].get('hostname')}\n")
                fp.write("  service: https://traefik.traefik.svc.cluster.local:443\n")
                fp.write("  originRequest:\n")
                fp.write("    noTLSVerify: true\n")
                fp.write('    originServerName: "*traefik*"\n')

        fp.write("- service: http_status:404\n")


if __name__ == "__main__":
    main()

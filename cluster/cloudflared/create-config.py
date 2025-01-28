import json
import subprocess

import yaml

# Run this script to generate the config map


def str_presenter(
    dumper: yaml.Dumper | yaml.representer.SafeRepresenter, data: str
) -> yaml.Node:
    """configures yaml for dumping multiline strings"""
    # https://github.com/yaml/pyyaml/issues/240#issuecomment-1096224358
    if data.count("\n") > 0:  # check for multiline string
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, str_presenter)
# to use with safe_dum
yaml.representer.SafeRepresenter.add_representer(str, str_presenter)


def main():
    # load DNS configs
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

    ingresses = []
    for dns_config in dns_configs["items"]:
        if dns_config["spec"].get("externalCNAME"):
            ingresses.append(
                {
                    "hostname": dns_config["spec"].get("hostname"),
                    "service": "https://traefik.traefik.svc.cluster.local:443",
                    "originRequest": {
                        "noTLSVerify": True,
                        "originServerName": "*traefik*",
                    },
                }
            )

    # sort other services
    ingresses = sorted(ingresses, key=lambda i: i["hostname"])

    # add 404 service at the end
    ingresses.append({"service": "http_status:404"})

    # create inner data object
    inner_data = {
        "tunnel": "k8s-tunnel",
        "credentials-file": "/etc/cloudflared/creds/credentials.json",
        "metrics": "0.0.0.0:2000",
        "no-autoupdate": True,
        "ingress": ingresses,
    }

    # convert to text
    inner_data_text = yaml.dump(inner_data, indent=2)

    # wrap with outer data
    outer_data = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {"name": "cloudflared-configmap", "namespace": "cloudflared"},
        "data": {"config.yaml": inner_data_text},
    }

    # write to file
    with open("configmap.yaml", "w") as fp:
        yaml.dump(outer_data, fp)


if __name__ == "__main__":
    main()

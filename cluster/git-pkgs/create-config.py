import pathlib

import yaml
import yaml.representer

THIS_DIR = pathlib.Path(__file__).parent
CLUSTER_DIR = THIS_DIR.parent

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


def main() -> None:
    repos = {}

    for yaml_file in CLUSTER_DIR.glob("**/*.y*ml"):
        with open(yaml_file) as fp:
            docs = yaml.safe_load_all(fp)
            for doc in docs:
                if not (
                    doc.get("apiVersion") == "source.toolkit.fluxcd.io/v1"
                    and doc.get("kind") == "HelmRepository"
                ):
                    continue

                print(f"Parsing {yaml_file}")

                repos[doc["metadata"].get("namespace")] = doc["spec"].get("url")

    # sort the repos
    repos = dict(sorted(repos.items()))

    # create inner data object
    inner_data = {
        "upstream": {
            "helm": repos,
            "generic": {
                "github": "https://github.com",
                "astral": "https://releases.astral.sh",
            },
            "oci": {"ghcr": "https://ghcr.io"},
        }
    }

    # convert to text
    inner_data_text = yaml.dump(inner_data, indent=2)

    # wrap with outer data
    outer_data = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {"name": "git-pkgs-configmap", "namespace": "git-pkgs"},
        "data": {"config.yaml": inner_data_text},
    }

    # write to file
    with open(THIS_DIR.joinpath("configmap.yaml"), "w") as fp:
        yaml.dump(outer_data, fp)


if __name__ == "__main__":
    main()

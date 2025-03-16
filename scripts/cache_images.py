import subprocess


def cache_image(image: str, i: int, total: int) -> None:
    """
    Cache an image
    """
    print(f"---- [{i}/{total}] Caching {image}")
    if not image.startswith("cr.nathanv.app"):
        image = f"cr.nathanv.app/{image}"

    subprocess.run(["docker", "pull", image])
    # subprocess.run(["docker", "image", "rm", new_image])


def normalize_image(image: str) -> str:
    """
    Normalize a container image name.
    ex:
    rancher/local-path-provisioner:v0.0.30 -> docker.io/rancher/local-path-provisioner:v0.0.30
    """

    # this is not 100% accurate, but it works for our use case
    chunks = image.split("/")
    # if there is no dot in the first chunk, assume it comes form docker hub
    if "." not in chunks[0]:
        return f"docker.io/{image}"

    # fine
    return image


def get_image_list() -> set[str]:
    """
    Return a list of all images used in the cluster
    """

    output = subprocess.check_output(
        [
            "kubectl",
            "get",
            "pods",
            "--all-namespaces",
            "-o",
            "jsonpath={.items[*].spec['initContainers', 'containers'][*].image}",
        ]
    ).decode("utf-8")
    # output is space seperated
    return set(output.split(" "))


if __name__ == "__main__":
    image_list = get_image_list()
    size = len(image_list)
    for i, image in enumerate(image_list):
        cache_image(normalize_image(image), i=i + 1, total=size)

import concurrent.futures
import json
import pathlib
import subprocess
import sys


def check_image(image_name: str) -> bool:
    """
    Checks if a Docker image has a manifest for amd64 architecture.
    """
    try:
        print("Checking image:", image_name, flush=True)
        result = subprocess.run(
            ["docker", "manifest", "inspect", image_name],
            capture_output=True,
            text=True,
            check=True,
        )
        manifest = json.loads(result.stdout)
        for entry in manifest.get("manifests", []):
            if entry.get("platform", {}).get("architecture") == "amd64":
                return True
        return False
    except subprocess.CalledProcessError:
        return False


def discover_images() -> list[str]:
    """
    Creates a list of of Docker images to check in the cluster directory.
    """
    cluster_dir = pathlib.Path(__file__).parent.parent.joinpath("cluster")
    images = set()

    for yml_file in cluster_dir.glob("**/*.y*ml"):
        with open(yml_file, "r") as f:
            for line in f:
                if "image:" in line and "#" not in line:
                    image = line.split("image:")[1].strip()
                    # skip blanks, probably from helm values
                    if not image:
                        continue

                    images.add(image)

    return list(images)


def main():
    images = discover_images()
    missing_amd64: list[str] = []

    # Check images concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Build a dictionary to map futures to image names
        future_to_image = {executor.submit(check_image, img): img for img in images}

        # Process completed futures
        for future in concurrent.futures.as_completed(future_to_image):
            image = future_to_image[future]
            if not future.result():
                missing_amd64.append(image)

    if missing_amd64:
        print(f"Images missing amd64 manifest:\n{'\n'.join(missing_amd64)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

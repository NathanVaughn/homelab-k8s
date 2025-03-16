import argparse
import pathlib
from typing import Literal

THIS_DIR = pathlib.Path(__file__).parent.parent
CLUSTER_DIR = THIS_DIR.joinpath("cluster")

PREFIX_APPLIED_FILE = CLUSTER_DIR.joinpath("PREFIX_APPLIED")

MARKER = "registry-proxy"
IMAGE_MARKER = "image-prefix"
BLOCK_START = "block-start"
BLOCK_END = "block-end"

REGISTRY = "cr.nathanv.app"

OPTIONS = Literal["add", "remove"]


def remove_image_prefix(line: str) -> str:
    parts = line.split("image: ", maxsplit=1)
    parts[1] = parts[1].replace(f"{REGISTRY}/", "")
    return "image: ".join(parts)


def add_image_prefix(line: str) -> str:
    parts = line.split("image: ", maxsplit=1)
    parts[1] = f"{REGISTRY}/{parts[1]}"
    return "image: ".join(parts)


def comment(line: str) -> str:
    content = line.lstrip()
    whitespace = line.removesuffix(content)
    return f"{whitespace}# {content}"


def uncomment(line: str) -> str:
    content = line.lstrip()
    whitespace = line.removesuffix(content)
    return f"{whitespace}{content.removeprefix('# ')}"


def process_lines(lines: list[str], mode: OPTIONS) -> tuple[list[str], bool]:
    # list of new lines to return
    new_lines = []
    # whether there were any changes
    changes = False

    # if the current line needs image prefix
    image_prefix_line = False
    # if the current line is inside a block
    block_line = False

    for line in lines:
        if MARKER in line:
            if IMAGE_MARKER in line:
                image_prefix_line = True
            elif BLOCK_START in line:
                block_line = True
            elif BLOCK_END in line:
                block_line = False

        elif image_prefix_line:
            changes = True
            image_prefix_line = False

            if mode == "remove":
                line = remove_image_prefix(line)
            elif mode == "add":
                line = add_image_prefix(line)

        elif block_line:
            changes = True

            if mode == "remove":
                line = comment(line)
            elif mode == "add":
                line = uncomment(line)

        new_lines.append(line)

    return new_lines, changes


def process_files(mode: OPTIONS):
    for yaml_file in CLUSTER_DIR.glob("**/*.yaml"):
        with yaml_file.open("r") as fp:
            lines = fp.readlines()

        new_lines, changes = process_lines(lines, mode)

        if changes:
            with yaml_file.open("w") as fp:
                fp.writelines(new_lines)

            print(f"Processed {yaml_file}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["add", "remove"])
    args = parser.parse_args()

    if args.action == "add":
        if PREFIX_APPLIED_FILE.exists():
            print("Prefix already applied")
            return

        process_files("add")
        PREFIX_APPLIED_FILE.touch()

    elif args.action == "remove":
        if not PREFIX_APPLIED_FILE.exists():
            print("Prefix already removed")
            return

        process_files("remove")
        PREFIX_APPLIED_FILE.unlink()


if __name__ == "__main__":
    main()

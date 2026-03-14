import sys

sys.path.append(".")

from scripts import common


def main(namespace: str, name: str):
    print(common.find_volume(namespace, name))


if __name__ == "__main__":
    namespace = input("Enter the PersistentVolumeClaim namespace: ").strip()
    name = input("Enter the PersistentVolumeClaim name: ").strip()

    main(namespace=namespace, name=name)

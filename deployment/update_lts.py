from pyinfra.operations import apt, python, server


def upgrade_lts() -> None:
    apt.update(name="Update apt cache", _sudo=True)
    apt.packages(
        name="Install update-manager-core",
        packages=["update-manager-core"],
        _sudo=True,
    )
    apt.upgrade(name="apt upgrade --autoremove", auto_remove=True, _sudo=True)
    server.shell(
        name="Upgrade the node",
        commands="do-release-upgrade -d -f DistUpgradeViewNonInteractive",
        _sudo=True,
    )


python.call(
    name="Upgrade Ubuntu LTS",
    function=upgrade_lts,
    _serial=True,
)

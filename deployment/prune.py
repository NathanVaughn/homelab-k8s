from pyinfra.operations import server

server.shell(
    name="Prune apt cache",
    commands="apt clean",
    _sudo=True,
)

server.shell(
    name="Prune apt partial files",
    commands="apt autoclean",
    _sudo=True,
)

server.shell(
    name="Prune images",
    commands="crictl rmi --prune",
    _sudo=True,
)

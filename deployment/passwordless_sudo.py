import io

from pyinfra import host
from pyinfra.facts.server import User
from pyinfra.operations import files

# setup passwordless sudo
files.block(
    name="Setup passwordless sudo",
    path="/etc/sudoers",
    content=f"{host.get_fact(User)} ALL=(ALL) NOPASSWD: ALL\n",
    _sudo=True,
)
# New way of doing this
files.put(
    name="Setup passwordless sudo",
    src=io.StringIO(f"{host.get_fact(User)} ALL=(ALL) NOPASSWD: ALL\n"),
    dest="/etc/sudoers.d/ubuntu",
    _sudo=True,
)

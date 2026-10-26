import io

from pyinfra import host
from pyinfra.facts.files import File
from pyinfra.facts.server import LsbRelease
from pyinfra.operations import files, server

lsb_info = host.get_fact(LsbRelease)
codename = lsb_info.get("codename") if lsb_info else None
assert codename is not None

sources_content = f"""Types: deb
URIs: https://pkgs.nathanv.app/debian/ubuntu/
Suites: {codename} {codename}-updates {codename}-backports
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

Types: deb
URIs: https://pkgs.nathanv.app/debian/ubuntu-security/
Suites: {codename}-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
"""

source_file = host.get_fact(File, path="/etc/apt/sources.list.d/ubuntu.sources")

if source_file:
    server.shell(
        name="Backup old ubuntu.sources",
        commands=[
            "mv /etc/apt/sources.list.d/ubuntu.sources /etc/apt/sources.list.d/ubuntu.sources.disabled"
        ],
        _sudo=True,
    )

files.put(
    name="Install mirrored Ubuntu sources file",
    src=io.StringIO(sources_content),
    dest="/etc/apt/sources.list.d/proxy.sources",
    _sudo=True,
)

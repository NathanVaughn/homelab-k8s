from pyinfra.operations import python, server, systemd

# https://docs.k3s.io/cli/certificate#rotating-client-and-server-certificates
# does not seem to happen automatically

# check with
# sudo k3s certificate check --output table


def rotate_certs():
    systemd.service(name="Stop k3s", service="k3s", running=False, _sudo=True)
    server.shell(
        name="Rotate k3s certificates", commands="k3s certificate rotate", _sudo=True
    )
    systemd.service(name="Start k3s", service="k3s", running=True, _sudo=True)


python.call(
    name="Rotate k3s certificates",
    function=rotate_certs,
    _serial=True,
)

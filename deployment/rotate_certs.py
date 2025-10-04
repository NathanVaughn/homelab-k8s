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


# alternative
# https://www.ibm.com/support/pages/expired-k3s-certificates-are-not-automatically-rotated-causing-connection-issues

# Resolving The Problem

# As a precautionary measure backup the TLS dir.
# `sudo tar -czvf /var/lib/rancher/k3s/server/apphost-cert.tar.gz /var/lib/rancher/k3s/server/tls`

# Remove the following file.
# `sudo rm /var/lib/rancher/k3s/server/tls/dynamic-cert.json`

# Remove the cached certificate from a kubernetes secret.
# `sudo kubectl --insecure-skip-tls-verify=true delete secret -n kube-system k3s-serving`

# Restart the K3s service to rotate the certificates.
# `sudo systemctl restart k3s`

# Verify that kubectl commands function.
# `sudo kubectl get pods -A`

# Additionally, you can verify that all K3s internal certificates are no longer due to expire.
# `sudo su`
# `for i in `ls /var/lib/rancher/k3s/server/tls/*.crt`; do echo $i; openssl x509 -enddate -noout -in $i; done`

# Or run
# `curl -v -k https://localhost:6443 [https://localhost:6443] to confirm the new date of your app host cert`

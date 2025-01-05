# PyInfra

## Setup

First, copy the K3S secret token into the `secrets/k3s_token` file.
Also, setup the S3 config file in `secrets/config.yaml` file.

To setup K3S, run the following command:

```bash
pyinfra inventory.py configure.py
```

May need to run

```bash
chmod go-r ~/.kube/config
```

After installation to fix permissions.

Now, bootstrap flux so the cluster is controlled by git:

```bash
flux bootstrap github --token-auth --owner=NathanVaughn --repository=homelab-k8s --branch=main --path=cluster/ --personal
```

## Updates

This will run package updates on all nodes. If nodes needs to be rebooted,
they will be drained and rebooted one-at-a-time.

```bash
pyinfra inventory.py update.py
```

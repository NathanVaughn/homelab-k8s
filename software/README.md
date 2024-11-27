To setup K3S, run the following command:

```bash
pyinfra inventory.py configure.py
```

Now, bootstrap flux so the cluster is controlled by git:

```bash
flux bootstrap github --token-auth --owner=NathanVaughn --repository=homelab-k8s --branch=main --path=cluster/ --personal
```

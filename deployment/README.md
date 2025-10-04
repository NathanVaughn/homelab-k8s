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

### Fail to join cluster

If a node fails to join the cluster:

```bash
# ssh into a different node
sudo su -
curl -LO https://github.com/etcd-io/etcd/releases/download/v3.5.18/etcd-v3.5.18-linux-amd64.tar.gz
tar -xzf etcd-v3.5.18-linux-amd64.tar.gz
cd ./etcd-v3.5.18-linux-amd64
export ETCDCTL_CACERT=/var/lib/rancher/k3s/server/tls/etcd/server-ca.crt
export ETCDCTL_CERT=/var/lib/rancher/k3s/server/tls/etcd/server-client.crt
export ETCDCTL_KEY=/var/lib/rancher/k3s/server/tls/etcd/server-client.key
export ETCDCTL_ENDPOINTS='https://127.0.0.1:2379'
export ETCDCTL_API=3

./etcdctl member list
# look at node list

./etcdctl member remove {node}
```

On the failed node:

```bash
sudo service k3s stop
sudo rm -rf /var/lib/rancher/
sudo rm -rf /etc/rancher/
# if needed
/usr/local/bin/k3s-killall.sh
```

Then try again.

## Updates

This will run package updates on all nodes. If nodes needs to be rebooted,
they will be drained and rebooted one-at-a-time.

```bash
pyinfra inventory.py update.py
```

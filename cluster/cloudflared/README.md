# Cloudflared

## Setup

[Install `cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).

```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
rm cloudflared-linux-amd64.deb
```

Now, login and create the tunnel:

```bash
cloudflared tunnel login
cloudflared tunnel create k8s-tunnel
cp ~/.cloudflared/*.json tunnel.json
cloudflared tunnel route dns k8s-tunnel tunnel.nathanv.app
```

Lastly, create a secret for the tunnel config:

```bash
kubectl apply -f namespace.yaml

kubectl -n cloudflared create secret generic tunnel-credentials \
--from-file=credentials.json=tunnel.json \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
```

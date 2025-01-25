# Factorio

Create a copy of `server-settings.example.json` and copy it to
`server-settings.json`.

## Setup

```bash
kubectl apply -f namespace.yaml

kubectl -n factorio create secret generic factorio-config \
--from-file=server-settings.json=server-settings.json \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml


export CLOUDFLARE_API_TOKEN=$CLOUDFLARE_API_TOKEN

kubectl -n factorio create secret generic factorio-ddns-env \
--from-literal=CLOUDFLARE_API_TOKEN=$CLOUDFLARE_API_TOKEN \ \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret2.yaml
# optional
kubectl apply -f sealed-secret2.yaml
```

## Post Setup

Set up a port forward in Omada for port `34197` to `10.0.1.5` for UDP traffic.

Configured under Site Settings -> Transmission -> NAT -> Port Forwarding.

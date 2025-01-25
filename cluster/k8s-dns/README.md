# k8s-dns

## Setup

```bash
export CLOUDFLARE_API_TOKEN=$CLOUDFLARE_API_TOKEN
export TECHNITIUM_API_TOKEN=$TECHNITIUM_API_TOKEN
kubectl apply -f namespace.yaml

kubectl -n k8s-dns create secret generic k8s-dns-env \
--from-literal=CLOUDFLARE_API_TOKEN=$CLOUDFLARE_API_TOKEN \
--from-literal=TECHNITIUM_API_TOKEN=$TECHNITIUM_API_TOKEN \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
```

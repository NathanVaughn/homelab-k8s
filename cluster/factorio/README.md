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
kubectl delete secret -n factorio factorio-config
```

# Traefik

## Setup

```bash
export TOKEN=$TOKEN
kubectl -n traefik create secret generic traefik-cf-token --from-literal=CF_DNS_API_TOKEN=$TOKEN --dry-run=client -o yaml > secret.yaml
kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
```

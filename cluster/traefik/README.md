# Traefik

## Setup

```bash
export CF_DNS_API_TOKEN=$CF_DNS_API_TOKEN
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

kubectl -n traefik create secret generic traefik-cf-token \
--from-literal=CF_DNS_API_TOKEN=$CF_DNS_API_TOKEN \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
kubectl delete secret -n traefik traefik-cf-token
```

# PHPMyAdmin

## Setup

```bash
export MARIADB_PASSWORD=$MARIADB_PASSWORD
kubectl apply -f namespace.yaml
kubectl -n bookstack create secret generic bookstack-env --from-literal=MARIADB_PASSWORD=$MARIADB_PASSWORD --from-literal=PMA_CONTROLPASS=$MARIADB_PASSWORD --dry-run=client -o yaml > secret.yaml
kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
```

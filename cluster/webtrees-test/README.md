# Webtrees

## Setup

```bash
export MARIADB_PASSWORD=$MARIADB_PASSWORD
kubectl apply -f namespace.yaml

kubectl -n webtrees-test create secret generic webtrees-test-env \
--from-literal=MARIADB_PASSWORD=$MARIADB_PASSWORD \
--from-literal=DB_PASS=$MARIADB_PASSWORD \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
```

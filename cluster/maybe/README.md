# Maybe

## Setup

```bash
export POSTGRES_PASSWORD=$POSTGRES_PASSWORD
export SECRET_KEY_BASE=$SECRET_KEY_BASE
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

kubectl -n maybe create secret generic maybe-env \
--from-literal=POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
--from-literal=SECRET_KEY_BASE=$SECRET_KEY_BASE \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
```

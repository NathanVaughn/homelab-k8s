# Maybe

## Setup

```bash
export POSTGRES_PASSWORD=$POSTGRES_PASSWORD
export SECRET_KEY_BASE=$SECRET_KEY_BASE
export SMTP_ADDRESS=$SMTP_ADDRESS
export SMTP_USERNAME=$SMTP_USERNAME
export SMTP_PASSWORD=$SMTP_PASSWORD
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

kubectl -n maybe create secret generic maybe-env \
--from-literal=POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
--from-literal=SECRET_KEY_BASE=$SECRET_KEY_BASE \
--from-literal=SMTP_ADDRESS=$SMTP_ADDRESS \
--from-literal=SMTP_USERNAME=$SMTP_USERNAME \
--from-literal=SMTP_PASSWORD=$SMTP_PASSWORD \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
kubectl delete secret -n maybe maybe-env
```

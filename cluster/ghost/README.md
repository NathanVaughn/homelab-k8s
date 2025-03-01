# Ghost

## Setup

```bash
export SMTP_HOST=$SMTP_HOST
export SMTP_USER=$SMTP_USER
export SMTP_PASSWORD=$SMTP_PASSWORD
export MYSQL_PASSWORD=$MYSQL_PASSWORD
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

kubectl -n ghost create secret generic ghost-env \
--from-literal=mail__options__host=$SMTP_HOST \
--from-literal=mail__options__auth__user=$SMTP_USER \
--from-literal=mail__options__auth__pass=$SMTP_PASSWORD \
--from-literal=database__connection__password=$MYSQL_PASSWORD \
--from-literal=MYSQL_PASSWORD=$MYSQL_PASSWORD \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
kubectl delete secret -n ghost ghost-env
```

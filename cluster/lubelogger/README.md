# LubeLogger

## Setup

```bash
export LUBELOGGER_EMAIL_HOST=$LUBELOGGER_EMAIL_HOST
export LUBELOGGER_EMAIL_USERNAME=$LUBELOGGER_EMAIL_USERNAME
export LUBELOGGER_EMAIL_PASSWORD=$LUBELOGGER_EMAIL_PASSWORD
kubectl apply -f namespace.yaml

kubectl -n lubelogger create secret generic lubelogger-secrets \
--from-literal=secret.emailServer=$LUBELOGGER_EMAIL_HOST \
--from-literal=secret.username=$LUBELOGGER_EMAIL_USERNAME \
--from-literal=secret.password=$LUBELOGGER_EMAIL_PASSWORD \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
```

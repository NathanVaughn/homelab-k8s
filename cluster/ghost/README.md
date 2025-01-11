# Ghost

## Setup

```bash
export SMTP_HOST=$SMTP_HOST
export SMTP_USER=$SMTP_USER
export SMTP_PASSWORD=$SMTP_PASSWORD
export MYSQL_AUTH_PASSWORD=$MYSQL_AUTH_PASSWORD
kubectl apply -f namespace.yaml
kubectl -n ghost create secret generic ghost-secrets --from-literal=smtpHost=$SMTP_HOST --from-literal=smtpUser=$SMTP_USER --from-literal=smtpPassword=$SMTP_PASSWORD --from-literal=mysql.auth.password=$MYSQL_AUTH_PASSWORD --dry-run=client -o yaml > secret.yaml
kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
```

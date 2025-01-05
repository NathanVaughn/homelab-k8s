# pgAdmin

## Setup

```bash
export PGADMIN_DEFAULT_EMAIL="$PGADMIN_DEFAULT_EMAIL"
export PGADMIN_DEFAULT_PASSWORD=$PGADMIN_DEFAULT_PASSWORD
# these need to include a literal quote
export PGADMIN_CONFIG_MAIL_SERVER='"$PGADMIN_CONFIG_MAIL_SERVER"'
export PGADMIN_CONFIG_MAIL_USERNAME='"$PGADMIN_CONFIG_MAIL_USERNAME"'
export PGADMIN_CONFIG_MAIL_PASSWORD='"$PGADMIN_CONFIG_MAIL_PASSWORD"'
kubectl apply -f namespace.yaml
kubectl -n pgadmin create secret generic pgadmin-env --from-literal=PGADMIN_DEFAULT_EMAIL=$PGADMIN_DEFAULT_EMAIL --from-literal=PGADMIN_DEFAULT_PASSWORD=$PGADMIN_DEFAULT_PASSWORD --from-literal=PGADMIN_CONFIG_MAIL_SERVER=$PGADMIN_CONFIG_MAIL_SERVER --from-literal=PGADMIN_CONFIG_MAIL_USERNAME=$PGADMIN_CONFIG_MAIL_USERNAME --from-literal=PGADMIN_CONFIG_MAIL_PASSWORD=$PGADMIN_CONFIG_MAIL_PASSWORD --dry-run=client -o yaml > secret.yaml
kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
```

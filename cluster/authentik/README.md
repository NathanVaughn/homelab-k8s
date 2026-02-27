# Authentik

## Setup

```bash
export AUTHENTIK_SECRET_KEY=$AUTHENTIK_SECRET_KEY
export POSTGRESQL_PASSWORD=$POSTGRESQL_PASSWORD
export AUTHENTIK_EMAIL_HOST=$AUTHENTIK_EMAIL_HOST
export AUTHENTIK_EMAIL_USERNAME=$AUTHENTIK_EMAIL_USERNAME
export AUTHENTIK_EMAIL_PASSWORD=$AUTHENTIK_EMAIL_PASSWORD
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

kubectl -n authentik create secret generic authentik-secrets \
--from-literal=authentik.secret_key=$AUTHENTIK_SECRET_KEY \
--from-literal=authentik.postgresql.password=$POSTGRESQL_PASSWORD \
--from-literal=postgresql.auth.password=$POSTGRESQL_PASSWORD \
--from-literal=authentik.email.host=$AUTHENTIK_EMAIL_HOST \
--from-literal=authentik.email.username=$AUTHENTIK_EMAIL_USERNAME \
--from-literal=authentik.email.password=$AUTHENTIK_EMAIL_PASSWORD \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
kubectl delete secret -n authentik authentik-secrets
```

## Database Size

Check table size with `\dt+` in the `psql` shell.

<https://github.com/goauthentik/authentik/issues/18139#issuecomment-3532818322>

```bash
TRUNCATE django_channels_postgres_message;
```
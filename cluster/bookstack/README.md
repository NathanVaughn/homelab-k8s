# Bookstack

## Setup

In Authentik, configure a OAuth2 provider. Use the redirect URL as
`https://bookstack.nathanv.app/oidc/callback`

```bash
export APP_KEY=$APP_KEY
export MARIADB_PASSWORD=$MARIADB_PASSWORD
export MAIL_HOST=$MAIL_HOST
export MAIL_USERNAME=$MAIL_USERNAME
export MAIL_PASSWORD=$MAIL_PASSWORD
export OIDC_CLIENT_ID=$OIDC_CLIENT_ID
export OIDC_CLIENT_SECRET=$OIDC_CLIENT_SECRET
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

kubectl -n bookstack create secret generic bookstack-env \
--from-literal=APP_KEY=$APP_KEY \
--from-literal=MARIADB_PASSWORD=$MARIADB_PASSWORD \
--from-literal=DB_PASSWORD=$MARIADB_PASSWORD \
--from-literal=MAIL_HOST=$MAIL_HOST \
--from-literal=MAIL_USERNAME=$MAIL_USERNAME \
--from-literal=MAIL_PASSWORD=$MAIL_PASSWORD \
--from-literal=OIDC_CLIENT_ID=$OIDC_CLIENT_ID \
--from-literal=OIDC_CLIENT_SECRET=$OIDC_CLIENT_SECRET \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
kubectl delete secret -n bookstack bookstack-env
```

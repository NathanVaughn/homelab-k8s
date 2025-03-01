# Paperless

## Setup

In Authentik, configure a OAuth2 provider. Use the redirect URL as
`https://paperless.nathanv.app/accounts/oidc/authentik/login/callback/`.

```bash
export POSTGRES_PASSWORD=$POSTGRES_PASSWORD
export PAPERLESS_SECRET_KEY=$PAPERLESS_SECRET_KEY
export PAPERLESS_EMAIL_HOST=$PAPERLESS_EMAIL_HOST
export PAPERLESS_EMAIL_HOST_USER=$PAPERLESS_EMAIL_HOST_USER
export PAPERLESS_EMAIL_HOST_PASSWORD=$PAPERLESS_EMAIL_HOST_PASSWORD
export CLIENT_ID=$CLIENT_ID
export CLIENT_SECRET=$CLIENT_SECRET
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

kubectl -n paperless create secret generic paperless-env \
--from-literal=POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
--from-literal=PAPERLESS_DBPASS=$POSTGRES_PASSWORD \
--from-literal=PAPERLESS_SECRET_KEY=$PAPERLESS_SECRET_KEY \
--from-literal=PAPERLESS_EMAIL_HOST=$PAPERLESS_EMAIL_HOST \
--from-literal=PAPERLESS_EMAIL_HOST_USER=$PAPERLESS_EMAIL_HOST_USER \
--from-literal=PAPERLESS_EMAIL_HOST_PASSWORD=$PAPERLESS_EMAIL_HOST_PASSWORD \
--from-literal=PAPERLESS_SOCIALACCOUNT_PROVIDERS="{\"openid_connect\":{\"APPS\":[{\"provider_id\":\"authentik\",\"name\":\"Authentik\",\"client_id\":\"$CLIENT_ID\",\"secret\":\"$CLIENT_SECRET\",\"settings\":{\"server_url\":\"https://authentik.nathanv.app/application/o/paperless/.well-known/openid-configuration\"}}],\"OAUTH_PKCE_ENABLED\":\"True\"}}" \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
kubectl delete secret -n paperless paperless-env
```

## Post Setup

After the first login, you'll need to manually make the new account a super user.
This is in the `auth_user` table.

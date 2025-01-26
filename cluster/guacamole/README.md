# Guacamole

## Setup

While the documentation is unclear, Guacamole Docker images come with all
SSO extensions pre-installed.

In Authentik, configure a OAuth2 provider. Use the redirect URL as
`https://guacamole.nathanv.app`

```bash
export OPENID_CLIENT_ID=$OPENID_CLIENT_ID
export POSTGRES_PASSWORD=$POSTGRES_PASSWORD
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

kubectl -n guacamole create secret generic guacamole-env \
--from-literal=POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
--from-literal=POSTGRESQL_PASSWORD=$POSTGRES_PASSWORD \
--from-literal=OPENID_CLIENT_ID=$OPENID_CLIENT_ID \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
```

## Post Setup

Set `EXTENSION_PRIORITY` to `*, openid`. This will allow you to sign in
with a username and password. The default account is `guacadmin` and `guacadmin`.
Create a user in the system with the same username as the Authentik user
and grant them full admin privileges.

You can now disable the `EXTENSION_PRIORITY` environment variable.

Log in with this account, and disable the built-in `guacadmin` account.

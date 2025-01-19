# Guacamole

## Setup

While the documentation is unclear, Guacamole Docker images come with all
SSO extensions pre-installed.

In Authentik, configure a OAuth2 provider. Use the redirect URL as
`https://guacamole.nathanv.app`

```bash
export OPENID_CLIENT_ID=$OPENID_CLIENT_ID
export POSTGRES_PASSWORD=$POSTGRES_PASSWORD
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

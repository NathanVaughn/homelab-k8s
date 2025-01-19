# Harbor

## Setup

In Authentik, configure a OAuth2 provider. Use the redirect URL as
`https://cr.nathanv.app/c/oidc/callback`

```bash
export ADMIN_PASSWORD=$ADMIN_PASSWORD
export REGISTRY_PASSWORD=$REGISTRY_PASSWORD
export DATABASE_PASSWORD=$DATABASE_PASSWORD
kubectl apply -f namespace.yaml

kubectl -n harbor create secret generic harbor-secrets \
--from-literal=harborAdminPassword=$ADMIN_PASSWORD \
--from-literal=registry.credentials.password=$REGISTRY_PASSWORD \
--from-literal=database.internal.password=$DATABASE_PASSWORD \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
```

## Post Setup

Configure an OIDC provider as follows:

- Endpoint: `https://authentik.nathanv.app/application/o/harbor/`
- OIDC Scope: `openid,profile,email`
- Username Claim: `preferred_username`

See <https://docs.goauthentik.io/integrations/services/harbor/> for more info.

For connecting to the database, the user is `postgres`.

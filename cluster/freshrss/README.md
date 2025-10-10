# Paperless

## Setup

In Authentik, configure a OAuth2 provider. Use the redirect URL as
`https://freshrss.nathanv.app/i/oidc/` as well as
`https://freshrss.nathanv.app:443/i/oidc/`.

```bash
export POSTGRES_PASSWORD=$POSTGRES_PASSWORD
export OIDC_CLIENT_ID=$OIDC_CLIENT_ID
export OIDC_CLIENT_SECRET=$OIDC_CLIENT_SECRET
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

kubectl -n freshrss create secret generic freshrss-env \
--from-literal=POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
--from-literal=DB_PASSWORD=$POSTGRES_PASSWORD \
--from-literal=OIDC_CLIENT_ID=$OIDC_CLIENT_ID \
--from-literal=OIDC_CLIENT_SECRET=$OIDC_CLIENT_SECRET \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
kubectl delete secret -n freshrss freshrss-env
```

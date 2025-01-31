# Actual

## Setup

In Authentik, configure a OAuth2 provider. Use the redirect URL as
`https://actual.nathanv.app/openid/callback`

```bash
export ACTUAL_OPENID_CLIENT_ID=$ACTUAL_OPENID_CLIENT_ID
export ACTUAL_OPENID_CLIENT_SECRET=$ACTUAL_OPENID_CLIENT_SECRET
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

kubectl -n actual create secret generic actual-env \
--from-literal=ACTUAL_OPENID_CLIENT_ID=$ACTUAL_OPENID_CLIENT_ID \
--from-literal=ACTUAL_OPENID_CLIENT_SECRET=$ACTUAL_OPENID_CLIENT_SECRET \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
```

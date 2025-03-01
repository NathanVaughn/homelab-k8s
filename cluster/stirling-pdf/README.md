# Stirling PDF

## Setup

In Authentik, configure a OAuth2 provider. Use the redirect URL as
`https://stirling-pdf.nathanv.app/login/oauth2/code/oidc`.

```bash
export SECURITY_OAUTH2_CLIENTID=$SECURITY_OAUTH2_CLIENT_ID
export SECURITY_OAUTH2_CLIENTSECRET=$SECURITY_OAUTH2_CLIENT_SECRET
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

kubectl -n stirling-pdf create secret generic stirling-pdf-env \
--from-literal=SECURITY_OAUTH2_CLIENTID=$SECURITY_OAUTH2_CLIENTID \
--from-literal=SECURITY_OAUTH2_CLIENTSECRET=$SECURITY_OAUTH2_CLIENTSECRET \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
```

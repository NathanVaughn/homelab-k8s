# Headlamp

## Setup

In Authentik, configure a OAuth2 provider.
Use the redirect URL as `https://headlamp.nathanv.app/oidc-callback`.

Change the "Access Token validity" in the Advanced protocol settings,
otherwise you will be constantly signed out.

```bash
export HEADLAMP_CONFIG_OIDC_CLIENT_ID=$HEADLAMP_CONFIG_OIDC_CLIENT_ID
export HEADLAMP_CONFIG_OIDC_CLIENT_SECRET=$HEADLAMP_CONFIG_OIDC_CLIENT_SECRET
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

kubectl -n headlamp create secret generic headlamp-secrets \
--from-literal=config.oidc.clientID=$HEADLAMP_CONFIG_OIDC_CLIENT_ID \
--from-literal=config.oidc.clientSecret=$HEADLAMP_CONFIG_OIDC_CLIENT_SECRET \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
```

See <https://elroy.fyi/posts/headlamp-setup-guide/> for more information.

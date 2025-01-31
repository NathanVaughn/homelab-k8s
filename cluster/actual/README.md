# pgAdmin

## Setup

In Authentik, configure a OAuth2 provider. Use the redirect URL as
`https://actual.nathanv.app/openid/callback`

Create a JSON file like below in order to setup OIDC Authentication as
`config.json`:

```json
{
"openId": {
        "issuer": "https://authentik.nathanv.app/application/o/actual/",
        "client_id": "client_id",
        "client_secret": "client_secret",
        "server_hostname": "actual.nathanv.app",
        "authMethod": "openid"
    }
}
```

```bash
kubectl apply -f namespace.yaml

kubectl -n actual create secret generic actual-oauth \
--from-file=config.json \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
```

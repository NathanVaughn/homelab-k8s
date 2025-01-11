# pgAdmin

## Setup

In Authentik, configure a OAuth2 provider. Use the redirect URL as
`https://pgadmin.nathanv.app/oauth2/authorize`

Create a Python file like below in order to setup OIDC Authentication as
`config_local.py`:

```python
OAUTH2_CONFIG = [
    {
        'OAUTH2_NAME': 'authentik',
        'OAUTH2_DISPLAY_NAME': 'Authentik',
        'OAUTH2_CLIENT_ID': 'TODO',
        'OAUTH2_CLIENT_SECRET': 'TODO',
        'OAUTH2_TOKEN_URL': 'https://authentik.nathanv.app/application/o/token/',
        'OAUTH2_AUTHORIZATION_URL': 'https://authentik.nathanv.app/application/o/authorize/',
        'OAUTH2_SERVER_METADATA_URL': None,
        'OAUTH2_API_BASE_URL': 'https://authentik.nathanv.app',
        'OAUTH2_USERINFO_ENDPOINT': 'https://authentik.nathanv.app/application/o/userinfo/',
        'OAUTH2_SCOPE': 'openid email profile name',
        'OAUTH2_USERNAME_CLAIM': 'email',
        'OAUTH2_ICON': 'fa-lock',
        'OAUTH2_BUTTON_COLOR': '#0000ff',
        'OAUTH2_ADDITIONAL_CLAIMS': None,
        'OAUTH2_SSL_CERT_VERIFICATION': True,
        'OAUTH2_LOGOUT_URL': 'https://authentik.nathanv.app/application/o/pgadmin/end-session/'
    }
]
```

```bash
export PGADMIN_DEFAULT_EMAIL="$PGADMIN_DEFAULT_EMAIL"
export PGADMIN_DEFAULT_PASSWORD=$PGADMIN_DEFAULT_PASSWORD
# these need to include a literal quote
export PGADMIN_CONFIG_MAIL_SERVER="'$PGADMIN_CONFIG_MAIL_SERVER'"
export PGADMIN_CONFIG_MAIL_USERNAME="'$PGADMIN_CONFIG_MAIL_USERNAME'"
export PGADMIN_CONFIG_MAIL_PASSWORD="'$PGADMIN_CONFIG_MAIL_PASSWORD'"
kubectl apply -f namespace.yaml
kubectl -n pgadmin create secret generic pgadmin-env --from-literal=PGADMIN_DEFAULT_EMAIL=$PGADMIN_DEFAULT_EMAIL --from-literal=PGADMIN_DEFAULT_PASSWORD=$PGADMIN_DEFAULT_PASSWORD --from-literal=PGADMIN_CONFIG_MAIL_SERVER=$PGADMIN_CONFIG_MAIL_SERVER --from-literal=PGADMIN_CONFIG_MAIL_USERNAME=$PGADMIN_CONFIG_MAIL_USERNAME --from-literal=PGADMIN_CONFIG_MAIL_PASSWORD=$PGADMIN_CONFIG_MAIL_PASSWORD --dry-run=client -o yaml > secret.yaml
kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml

kubectl -n pgadmin create secret generic pgadmin-oauth --from-file=config_local.py --dry-run=client -o yaml > secret.yaml
kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret2.yaml
```

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
        'OAUTH2_CLIENT_ID': '{TODO}',
        'OAUTH2_CLIENT_SECRET': '{TODO}',
        'OAUTH2_TOKEN_URL': 'https://authentik.nathanv.app/application/o/token/',
        'OAUTH2_AUTHORIZATION_URL': 'https://authentik.nathanv.app/application/o/authorize/',
        'OAUTH2_SERVER_METADATA_URL': 'https://authentik.nathanv.app/application/o/pgadmin/.well-known/openid-configuration',
        'OAUTH2_API_BASE_URL': 'https://authentik.nathanv.app',
        'OAUTH2_USERINFO_ENDPOINT': 'https://authentik.nathanv.app/application/o/userinfo/',
        'OAUTH2_SCOPE': 'openid email profile name',
        'OAUTH2_USERNAME_CLAIM': 'email',
        'OAUTH2_ICON': 'fa-hive',
        'OAUTH2_BUTTON_COLOR': '#0000ff',
        'OAUTH2_ADDITIONAL_CLAIMS': None,
        'OAUTH2_SSL_CERT_VERIFICATION': True,
        'OAUTH2_LOGOUT_URL': 'https://authentik.nathanv.app/application/o/pgadmin/end-session/'
    }
]
```

```bash
export POSTGRES_PASSWORD=$POSTGRES_PASSWORD
export PGADMIN_DEFAULT_EMAIL="$PGADMIN_DEFAULT_EMAIL"
export PGADMIN_DEFAULT_PASSWORD=$PGADMIN_DEFAULT_PASSWORD
# these need to include a literal quote
export PGADMIN_CONFIG_MAIL_SERVER="'$PGADMIN_CONFIG_MAIL_SERVER'"
export PGADMIN_CONFIG_MAIL_USERNAME="'$PGADMIN_CONFIG_MAIL_USERNAME'"
export PGADMIN_CONFIG_MAIL_PASSWORD="'$PGADMIN_CONFIG_MAIL_PASSWORD'"
export PGADMIN_CONFIG_CONFIG_DATABASE_URI="'postgresql://pgadmin:$POSTGRES_PASSWORD@pgadmin-postgresql-service.pgadmin.svc.cluster.local:5432/pgadmin'"
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

# SETUP environment variables also set
# Docker ones don't seem to work when using postgres backend
# https://github.com/pgadmin-org/pgadmin4/blob/a9974b418c49760d3989b7fb25e052ff16b89ac6/web/pgadmin/setup/user_info.py#L37-L44
kubectl -n pgadmin create secret generic pgadmin-env \
--from-literal=POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
--from-literal=PGADMIN_DEFAULT_EMAIL=$PGADMIN_DEFAULT_EMAIL \
--from-literal=PGADMIN_DEFAULT_PASSWORD=$PGADMIN_DEFAULT_PASSWORD \
--from-literal=PGADMIN_SETUP_EMAIL=$PGADMIN_DEFAULT_EMAIL \
--from-literal=PGADMIN_SETUP_PASSWORD=$PGADMIN_DEFAULT_PASSWORD \
--from-literal=PGADMIN_CONFIG_MAIL_SERVER=$PGADMIN_CONFIG_MAIL_SERVER \
--from-literal=PGADMIN_CONFIG_MAIL_USERNAME=$PGADMIN_CONFIG_MAIL_USERNAME \
--from-literal=PGADMIN_CONFIG_MAIL_PASSWORD=$PGADMIN_CONFIG_MAIL_PASSWORD \
--from-literal=PGADMIN_CONFIG_CONFIG_DATABASE_URI=$PGADMIN_CONFIG_CONFIG_DATABASE_URI \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml

kubectl -n pgadmin create secret generic pgadmin-oauth \
--from-file=config_local.py \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret2.yaml
```

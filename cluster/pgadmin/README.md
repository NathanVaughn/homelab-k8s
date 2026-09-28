# pgAdmin

## Setup

In Authentik, configure a OAuth2 provider. Use the redirect URL as
`https://pgadmin.nathanv.app/oauth2/authorize`

Create a Python file like below in order to setup OIDC Authentication as
`config_local.py`:

```python
OAUTH2_CONFIG = [
    {
        "OAUTH2_NAME": "authentik",
        "OAUTH2_DISPLAY_NAME": "Authentik",
        "OAUTH2_CLIENT_ID": "{TODO}",
        "OAUTH2_CLIENT_SECRET": "{TODO}",
        "OAUTH2_TOKEN_URL": "https://authentik.nathanv.app/application/o/token/",
        "OAUTH2_AUTHORIZATION_URL": "https://authentik.nathanv.app/application/o/authorize/",
        "OAUTH2_SERVER_METADATA_URL": "https://authentik.nathanv.app/application/o/pgadmin/.well-known/openid-configuration",
        "OAUTH2_API_BASE_URL": "https://authentik.nathanv.app",
        "OAUTH2_USERINFO_ENDPOINT": "https://authentik.nathanv.app/application/o/userinfo/",
        "OAUTH2_SCOPE": "openid email profile name",
        "OAUTH2_USERNAME_CLAIM": "email",
        "OAUTH2_ICON": "fa-hive",
        "OAUTH2_BUTTON_COLOR": "#0000ff",
        "OAUTH2_ADDITIONAL_CLAIMS": None,
        "OAUTH2_SSL_CERT_VERIFICATION": True,
        "OAUTH2_LOGOUT_URL": "https://authentik.nathanv.app/application/o/pgadmin/end-session/",
    }
]
```

## Bitwarden secrets

- `PGADMIN_ADMIN_EMAIL`
- `PGADMIN_ADMIN_PASSWORD`
- `PGADMIN_DB_DATABASE`
- `PGADMIN_DB_PASSWORD`
- `PGADMIN_DB_USERNAME`
- `PGADMIN_OIDC_CLIENT_ID`
- `PGADMIN_OIDC_CLIENT_SECRET`
- `PGADMIN_SMTP_HOST`
- `PGADMIN_SMTP_PASSWORD`
- `PGADMIN_SMTP_USERNAME`

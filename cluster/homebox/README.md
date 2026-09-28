# Homebox

## Setup

In Authentik, configure a OAuth2 provider. Use the redirect URL as
`https://homebox.nathanv.app/api/v1/users/login/oidc/callback`

## Bitwarden secrets

- `HOMEBOX_SECRET_KEY` (random secret, at least 32 characters, e.g. `openssl rand -base64 48`)
- `HOMEBOX_DB_DATABASE`
- `HOMEBOX_DB_PASSWORD`
- `HOMEBOX_DB_USERNAME`
- `HOMEBOX_OIDC_CLIENT_ID`
- `HOMEBOX_OIDC_CLIENT_SECRET`
- `HOMEBOX_SMTP_HOST`
- `HOMEBOX_SMTP_PASSWORD`
- `HOMEBOX_SMTP_USERNAME`

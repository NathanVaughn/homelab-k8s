# LubeLogger

## Setup

In Authentik, configure a OAuth2 provider. Use the redirect URL as
`https://lubelogger.nathanv.app/Login/RemoteAuth`

## Bitwarden secrets

- `LUBELOGGER_DB_DATABASE`
- `LUBELOGGER_DB_PASSWORD`
- `LUBELOGGER_DB_USERNAME`
- `LUBELOGGER_OIDC_CLIENT_ID`
- `LUBELOGGER_OIDC_CLIENT_SECRET`
- `LUBELOGGER_SMTP_HOST`
- `LUBELOGGER_SMTP_PASSWORD`
- `LUBELOGGER_SMTP_USERNAME`

## Post Setup

The first time you log, you'll be asked for a token. You will need
to manually add this token to the database in the `tokenrecords` table.
It can be any value, though a GUID is recommended. Use anything other than `0`
for the ID, and the email must match exactly.

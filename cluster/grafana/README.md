# Grafana

## Setup

In Authentik, configure a OAuth2 provider. Use the redirect URL as
`https://grafana.nathanv.app/login/generic_oauth`

## Bitwarden secrets

- `GRAFANA_ADMIN_PASSWORD`
- `GRAFANA_ADMIN_USER`
- `GRAFANA_DB_DATABASE`
- `GRAFANA_DB_PASSWORD`
- `GRAFANA_DB_USERNAME`
- `GRAFANA_OIDC_CLIENT_ID`
- `GRAFANA_OIDC_CLIENT_SECRET`
- `GRAFANA_SMTP_HOST`
- `GRAFANA_SMTP_PASSWORD`
- `GRAFANA_SMTP_USERNAME`

## Post Setup

Set `grafana.ini.auth.generic_oauth.auto_login` to `false`.
This will allow you to sign in with a username and password.
Log in with Authentik, log out, and then log in as admin using username and password.
Make the Authentik user an admin, along with an admin in the default org.
Disable the builtin admin account and log out.

You can now reset `grafana.ini.auth.generic_oauth.auto_login` to `true`.

Add the following as a datasource:
`http://prometheus-kube-prometheus-prometheus.prometheus.svc.cluster.local:9090`

# Grafana

## Setup

In Authentik, configure a OAuth2 provider. Use the redirect URL as
`https://grafana.nathanv.app/login/generic_oauth`

```bash
# admin user cannot be same as Authentik user
export ADMIN_USER=$ADMIN_USER
export ADMIN_PASSWORD=$ADMIN_PASSWORD
export OAUTH_CLIENT_ID=$OAUTH_CLIENT_ID
export OAUTH_CLIENT_SECRET=$OAUTH_CLIENT_SECRET
export SMTP_HOST=$SMTP_HOST
export SMTP_USER=$SMTP_USER
export SMTP_PASSWORD=$SMTP_PASSWORD
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

kubectl -n grafana create secret generic grafana-secrets \
--from-literal=adminUser=$ADMIN_USER \
--from-literal=adminPassword=$ADMIN_PASSWORD \
--from-literal=grafana_ini.auth_generic_oauth.client_id=$OAUTH_CLIENT_ID \
--from-literal=grafana_ini.auth_generic_oauth.client_secret=$OAUTH_CLIENT_SECRET \
--from-literal=grafana_ini.smtp.host=$SMTP_HOST \
--from-literal=grafana_ini.smtp.user=$SMTP_USER \
--from-literal=grafana_ini.smtp.password=$SMTP_PASSWORD \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
```

## Post Setup

Set `grafana.ini.auth.generic_oauth.auto_login` to `false`.
This will allow you to sign in with a username and password.
Log in with Authentik, log out, and then log in as admin using username and password.
Make the Authentik user an admin, along with an admin in the default org.
Disable the builtin admin account and log out.

You can now reset `grafana.ini.auth.generic_oauth.auto_login` to `true`.

Add the following as a datasource:
`http://prometheus-kube-prometheus-prometheus.prometheus.svc.cluster.local:9090`

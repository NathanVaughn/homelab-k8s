# LubeLogger

## Setup

In Authentik, configure a OAuth2 provider. Use the redirect URL as
`https://lubelogger.nathanv.app/Login/RemoteAuth`

```bash
export POSTGRES_PASSWORD=$POSTGRES_PASSWORD
export POSTGRES_CONNECTION="Host=lubelogger-postgresql-service.lubelogger.svc.cluster.local:5432;Username=lubelogger;Password=$POSTGRES_PASSWORD;Database=lubelogger;"
export MAILCONFIG_EMAILSERVER=$MAILCONFIG_EMAILSERVER
export MAILCONFIG_USERNAME=$MAILCONFIG_USERNAME
export MAILCONFIG_PASSWORD=$MAILCONFIG_PASSWORD
export OPENIDCONFIG_CLIENTID=$OPENIDCONFIG_CLIENTID
export OPENIDCONFIG_SECRET=$OPENIDCONFIG_SECRET
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

kubectl -n lubelogger create secret generic lubelogger-env \
--from-literal=POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
--from-literal=POSTGRES_CONNECTION=$POSTGRES_CONNECTION \
--from-literal=MailConfig__EmailServer=$MAILCONFIG_EMAILSERVER \
--from-literal=MailConfig__Username=$MAILCONFIG_USERNAME \
--from-literal=MailConfig__Password=$MAILCONFIG_PASSWORD \
--from-literal=OpenIDConfig__ClientId=$OPENIDCONFIG_CLIENTID \
--from-literal=OpenIDConfig__ClientSecret=$OPENIDCONFIG_SECRET \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
kubectl delete secret -n lubelogger lubelogger-env
```

## Post Setup

The first time you log, you'll be asked for a token. You will need
to manually add this token to the database in the `tokenrecords` table.
It can be any value, though a GUID is recommended. Use anything other than `0`
for the ID, and the email must match exactly.

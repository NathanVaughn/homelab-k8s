# PHPMyAdmin

## Setup

In Authentik, create a proxy provider for a single application with the URL
`https://phpmyadmin.nathanv.app`. Ensure you assign the application to an outpost.

```bash
export MARIADB_PASSWORD=$MARIADB_PASSWORD
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

kubectl -n phpmyadmin create secret generic phpmyadmin-env \
--from-literal=MARIADB_PASSWORD=$MARIADB_PASSWORD \
--from-literal=PMA_CONTROLPASS=$MARIADB_PASSWORD \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
```

## Post Setup

After starting the service for the first time, log in and create the PHPMyAdmin
tables in the web UI. There will be a button prompt.

# Prometheus

In Authentik, create a proxy provider for a single application with the URL
`https://prometheus.nathanv.app`. Ensure you assign the application to an outpost.

In Authentik, create a proxy provider for a single application with the URL
`https://alertmanager.nathanv.app`. Ensure you assign the application to an outpost.

## Setup

```bash
export EMAIL_HOST_AND_PORT=$EMAIL_HOST_AND_PORT
export EMAIL_USERNAME=$EMAIL_USERNAME
export EMAIL_PASSWORD=$EMAIL_PASSWORD
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

kubectl -n prometheus create secret generic alertmanager-secrets \
--from-literal=alertmanager.config.global.smtp_smarthost=$EMAIL_HOST_AND_PORT \
--from-literal=alertmanager.config.global.smtp_auth_username=$EMAIL_USERNAME \
--from-literal=alertmanager.config.global.smtp_auth_password=$EMAIL_PASSWORD \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
kubectl delete secret -n prometheus alertmanager-secrets
```

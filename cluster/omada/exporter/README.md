# Omada Exporter

## Setup

In the Omada controller, create a user called `prometheus` as a Viewer.

```bash
export OMADA_PROMETHEUS_PASSWORD=$OMADA_PROMETHEUS_PASSWORD
# change dollar sign variables above this line

kubectl -n omada create secret generic omada-exporter-env \
--from-literal=OMADA_PASS=$OMADA_PROMETHEUS_PASSWORD \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
kubectl delete secret -n omada omada-exporter-env
```

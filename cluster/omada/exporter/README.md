# Omada Exporter

Not using Helm chart because of <https://github.com/charlie-haley/charts/pull/11>
and <https://github.com/charlie-haley/omada_exporter/issues/101>.

## Setup

In the Omada controller, create a user called `prometheus` as a Viewer.

Additionally, go to Settings -> Platform Integration, and create an OpenAPI app.
Use the "client" mode, and give it viewer permissions.

```bash
export OMADA_PROMETHEUS_PASSWORD=$OMADA_PROMETHEUS_PASSWORD
export OMADA_CLIENT_ID=$OMADA_CLIENT_ID
export OMADA_SECRET_ID=$OMADA_SECRET_ID
# change dollar sign variables above this line

kubectl -n omada create secret generic omada-exporter-env \
--from-literal=OMADA_PASS=$OMADA_PROMETHEUS_PASSWORD \
--from-literal=OMADA_CLIENT_ID=$OMADA_CLIENT_ID \
--from-literal=OMADA_SECRET_ID=$OMADA_SECRET_ID \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
kubectl delete secret -n omada omada-exporter-env
```

# ADS-B

## Setup

In Authentik, create a proxy provider for a single application with the URL
`https://readsb.nathanv.app`. Ensure you assign the application to an outpost.

```bash
export FLIGHT_AWARE_FEEDER_ID=$FLIGHT_AWARE_FEEDER_ID
export FR24KEY=$FR24KEY
export PLANE_FINDER_CODE=$PLANE_FINDER_CODE
export READSB_LAT=$READSB_LAT
export READSB_LON=$READSB_LON
kubectl apply -f namespace.yaml

kubectl -n adsb create secret generic adsb-env \
--from-literal=FEEDER_ID=$FLIGHT_AWARE_FEEDER_ID \
--from-literal=FR24KEY=$FR24KEY \
--from-literal=SHARECODE=$PLANE_FINDER_CODE \
--from-literal=READSB_LAT=$READSB_LAT \
--from-literal=READSB_LON=$READSB_LON \
--from-literal=LAT=$READSB_LAT \
--from-literal=LONG=$READSB_LON \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
```

## Create secret manifest

```bash
# generate manifest
kubectl -n netdata create secret generic netdata-secrets --from-file=values.yaml --dry-run=client -o yaml > secrets.yaml
# seal manifest
kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secrets.yaml > secrets-sealed.yaml
rm secrets.yaml # optional
# apply
kubectl apply -f secrets-sealed.yaml
```
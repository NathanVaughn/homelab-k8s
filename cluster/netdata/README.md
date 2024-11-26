## Create secret manifest

```bash
export TOKEN=$TOKEN
export ROOMS=$ROOMS
# generate manifest
kubectl -n netdata create secret generic netdata-secrets --from-literal=parent.claiming.token=$TOKEN --from-literal=child.claiming.token=$TOKEN --from-literal=parent.claiming.rooms=$ROOMS --from-literal=child.claiming.rooms=$ROOMS --dry-run=client -o yaml > secrets.yaml
# seal manifest
kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secrets.yaml > secrets-sealed.yaml
rm secrets.yaml # optional
# apply
kubectl apply -f secrets-sealed.yaml
```
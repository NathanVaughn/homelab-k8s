# Longhorn

## Setup

```bash
export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
export AWS_ENDPOINTS=s3.us-west-001.backblazeb2.com
export VIRTUAL_HOSTED_STYLE=false
kubectl -n longhorn create secret generic longhorn-env --from-literal=AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --from-literal=AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY --from-literal=AWS_ENDPOINTS=$AWS_ENDPOINTS --from-literal=VIRTUAL_HOSTED_STYLE=$VIRTUAL_HOSTED_STYLE --dry-run=client -o yaml > secret.yaml
kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
```

## Post launch

All persistent volume claims should use the storage class name "longhorn".

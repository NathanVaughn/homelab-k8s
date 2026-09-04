# Ghost

## Setup

```bash
export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
export AWS_REGION=$AWS_REGION
export POSTGRES_PASSWORD=$DB_PASSWORD
export S3_BUCKET=$S3_BUCKET
export S3_ENDPOINT=$S3_ENDPOINT
export PROXY_STORAGE_DIRECT_SERVE=true
export PROXY_STORAGE_DIRECT_SERVE_BASE_URL=$PROXY_STORAGE_DIRECT_SERVE_BASE_URL
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

kubectl -n git-pkgs create secret generic git-pkgs-env \
--from-literal=AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
--from-literal=AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
--from-literal=AWS_REGION=$AWS_REGION \
--from-literal=PROXY_DATABASE_URL=postgres://gitpkgs:$POSTGRES_PASSWORD@git-pkgs-postgresql-service.git-pkgs.svc.cluster.local:5432/gitpkgs?sslmode=disable \
--from-literal="PROXY_STORAGE_URL=s3://$S3_BUCKET?endpoint=$S3_ENDPOINT&prefix=pkgs/&use_path_style=false" \
--from-literal=POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
--from-literal=PROXY_STORAGE_DIRECT_SERVE=$PROXY_STORAGE_DIRECT_SERVE \
--from-literal=PROXY_STORAGE_DIRECT_SERVE_BASE_URL=$PROXY_STORAGE_DIRECT_SERVE_BASE_URL \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
kubectl delete secret -n git-pkgs git-pkgs-env
```

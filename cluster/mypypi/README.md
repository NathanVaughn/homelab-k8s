# MyPyPi

## Setup

```bash
export POSTGRES_PASSWORD=$POSTGRES_PASSWORD
export S3_ACCESS_KEY_ID=$S3_ACCESS_KEY_ID
export S3_SECRET_ACCESS_KEY=$S3_SECRET_ACCESS_KEY
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

kubectl -n mypypi create secret generic mypypi-env \
--from-literal=POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
--from-literal=MYPYPI_DATABASE__URL=postgresql://mypypi:$POSTGRES_PASSWORD@mypypi-postgresql-service.mypypi.svc.cluster.local/mypypi \
--from-literal=MYPYPI_STORAGE__S3__ACCESS_KEY_ID=$S3_ACCESS_KEY_ID \
--from-literal=MYPYPI_STORAGE__S3__SECRET_ACCESS_KEY=$S3_SECRET_ACCESS_KEY \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
kubectl delete secret -n mypypi mypypi-env
```

## Data Corruption

If a package gets corrupted:

```sql
DELETE FROM metadata_file_hash
WHERE metadata_file_id IN (
    SELECT id
    FROM metadata_file
    WHERE filename LIKE 'name%'
);

DELETE FROM metadata_file
WHERE filename LIKE 'name%';

DELETE FROM code_file_hash
WHERE code_file_id IN (
    SELECT id
    FROM code_file
    WHERE filename LIKE 'name%'
);

DELETE FROM code_file
WHERE filename LIKE 'name%';

DELETE FROM package
WHERE name = 'name';
```

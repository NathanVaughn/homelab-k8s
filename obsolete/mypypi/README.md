# MyPyPi

## Setup

## Bitwarden secrets

- `MYPYPI_DB_DATABASE`
- `MYPYPI_DB_PASSWORD`
- `MYPYPI_DB_USERNAME`
- `MYPYPI_S3_ACCESS_KEY_ID`
- `MYPYPI_S3_BUCKET`
- `MYPYPI_S3_ENDPOINT`
- `MYPYPI_S3_REGION`
- `MYPYPI_S3_SECRET_ACCESS_KEY`

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

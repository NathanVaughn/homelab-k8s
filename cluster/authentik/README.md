# Authentik

## Bitwarden secrets

- `AUTHENTIK_DB_DATABASE`
- `AUTHENTIK_DB_PASSWORD`
- `AUTHENTIK_DB_USERNAME`
- `AUTHENTIK_SECRET_KEY`
- `AUTHENTIK_SMTP_HOST`
- `AUTHENTIK_SMTP_PASSWORD`
- `AUTHENTIK_SMTP_USERNAME`

## Database Size

Check table size with `\dt+` in the `psql` shell.

```bash
kubectl exec --stdin --tty -n authentik authentik-postgresql-0 -- /bin/bash
psql -U authentik -d authentik
```

<https://github.com/goauthentik/authentik/issues/18139#issuecomment-3532818322>
<https://github.com/goauthentik/authentik/issues/19302>
<https://github.com/goauthentik/authentik/issues/19299>

```sql
TRUNCATE TABLE django_channels_postgres_message;
```

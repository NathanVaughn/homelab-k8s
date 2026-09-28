# PHPMyAdmin

## Setup

In Authentik, create a proxy provider for a single application with the URL
`https://phpmyadmin.nathanv.app`. Ensure you assign the application to an outpost.

## Bitwarden secrets

- `PHPMYADMIN_DB_DATABASE`
- `PHPMYADMIN_DB_PASSWORD`
- `PHPMYADMIN_DB_USERNAME`

## Post Setup

After starting the service for the first time, log in and create the PHPMyAdmin
tables in the web UI. There will be a button prompt.

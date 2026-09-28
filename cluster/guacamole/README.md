# Guacamole

## Setup

While the documentation is unclear, Guacamole Docker images come with all
SSO extensions pre-installed.

In Authentik, configure a OAuth2 provider. Use the redirect URL as
`https://guacamole.nathanv.app`

## Bitwarden secrets

- `GUACAMOLE_DB_DATABASE`
- `GUACAMOLE_DB_PASSWORD`
- `GUACAMOLE_DB_USERNAME`
- `GUACAMOLE_OIDC_CLIENT_ID`

## Post Setup

Set `EXTENSION_PRIORITY` to `*, openid`. This will allow you to sign in
with a username and password. The default account is `guacadmin` and `guacadmin`.
Create a user in the system with the same username as the Authentik user
and grant them full admin privileges.

You can now disable the `EXTENSION_PRIORITY` environment variable.

Log in with this account, and disable the built-in `guacadmin` account.

When adding connections, just use the hostname (`annie`),
not the fully qualified domain name (`annie.nathanv.home`).
These are already hardcoded in the CoreDNS config, but forwarding to the upstream
home DNS server seems inconsistent.

# Harbor

## Setup

In Authentik, configure a OAuth2 provider. Use the redirect URL as
`https://cr.nathanv.app/c/oidc/callback`

Change the "Access Token validity" in the Advanced protocol settings,
otherwise you will be constantly signed out.

## Bitwarden secrets

- `HARBOR_ADMIN_PASSWORD`
- `HARBOR_DB_PASSWORD`
- `HARBOR_REGISTRY_PASSWORD`

## Post Setup

Configure an OIDC provider as follows:

- Endpoint: `https://authentik.nathanv.app/application/o/harbor/`
- OIDC Scope: `openid,profile,email`
- Username Claim: `preferred_username`

See <https://docs.goauthentik.io/integrations/services/harbor/> for more info.

For connecting to the database, the user is `postgres`.

# Portainer

## Setup

In Authentik, configure a OAuth2 provider. Use the redirect URL as
`https://portainer.nathanv.app`.

## Post Setup

Configure an OAuth provider as follows:

Authorization URL: `https://authentik.nathanv.app/application/o/authorize/`
Access Token URL: `[openid,profile,email](https://authentik.nathanv.app/application/o/token/)`
Resource URL: `https://authentik.nathanv.app/application/o/userinfo/`
Redirect URL: `https://portainer.nathanv.app`
Logout URL: `https://authentik.nathanv.app/application/o/portainer/end-session/`
User Identifier: `preferred_username`
Scopes: `email openid profile`

See <https://docs.goauthentik.io/integrations/services/portainer/> for more info.

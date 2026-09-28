# Headlamp

## Setup

Go to Customization -> Property Mappings. Create a new "Scope Mapping". Set the scope
name to "email" and the Expression as:

```python
return {
    "email": user.email,
    "email_verified": True,
}
```

<https://docs.goauthentik.io/add-secure-apps/providers/property-mappings/#scope-mappings-with-oauth2>.

In Authentik, configure a OAuth2 provider.
Use the redirect URL as `https://headlamp.nathanv.app/oidc-callback`.
Add the new scope to the provider scopes under "Advanced protocol settings".

Change the "Access Token validity" in the Advanced protocol settings,
otherwise you will be constantly signed out.

## Bitwarden secrets

- `HEADLAMP_OIDC_CLIENT_ID`
- `HEADLAMP_OIDC_CLIENT_SECRET`

See <https://elroy.fyi/posts/headlamp-setup-guide/> for more information.

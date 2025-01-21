# Technitium DNS

## Setup

In Authentik, create a proxy provider for a single application with the URL
`https://technitium-dns.nathanv.app`. Ensure you assign the application to an outpost.

## Post Setup

### Auth

The default login is `admin` and `admin`. You can create a new user
and give them super admin privileges, then disable the default account.

### Zones

Create a Primary Zone for `nathanv.home`. Configure services and node names
as described in the IP address docs.

Create a Conditional Forwarder Zone for `nathanv.app`. Select 'Use "This Server"'
under the Forwarder options.

### Blocklists

Under Allowed, add the following domain names:

Vimeo:

- player-telemetry.vimeo.com
- f.vimeocdn.com
- collector.vhx.tv

Azure DevOps:

- 37bvsblobprodcus311.blob.core.windows.net

Under Blocked, add the following domain names:

- tttturl.com

Under Settings -> Blocking, add the following blocklists:

- <https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/pro.txt>
- <https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/fake.txt>

### Apps

Install "Query Logs (Sqlite)".

### Misc

DNS over HTTPS can be enabled under Settings -> Optional Protocols.

The hostname and default contact email can modified under Settings -> General.

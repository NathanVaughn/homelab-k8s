# Technitium DNS

## Setup

In Authentik, create a proxy provider for a single application with the URL
`https://technitium-dns.nathanv.app`. Ensure you assign the application to an outpost.

## Bitwarden secrets

- `TECHNITIUM_DNS_DB_DATABASE`
- `TECHNITIUM_DNS_DB_PASSWORD`
- `TECHNITIUM_DNS_DB_USERNAME`

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

- `player-telemetry.vimeo.com`
- `f.vimeocdn.com`
- `collector.vhx.tv`

Azure DevOps:

- `37bvsblobprodcus311.blob.core.windows.net`

Under Blocked, add the following domain names:

- `tttturl.com`

Under Settings -> Blocking, add the following blocklists:

- <https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/pro.txt>
- <https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/fake.txt>

### Apps

Install "Query Logs (PostgreSQL)".
Change the configuration:

```json
{
  "enableLogging": true,
  "maxQueueSize": 1000000,
  "maxLogDays": 30,
  "maxLogRecords": 0,
  "databaseName": "technitiumdns",
  "connectionString": "Server=technitium-dns-postgresql-service.technitium-dns.svc.cluster.local; Port=5432; Username=technitiumdns; Password=$POSTGRES_PASSWORD;"
}
```

Cannot use a dash in the database name.

### Misc

The hostname and default contact email can modified under Settings -> General.

To clear out old stat files, run `rm /etc/dns/stats/{year}*`

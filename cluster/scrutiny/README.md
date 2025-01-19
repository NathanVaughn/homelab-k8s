# Scrutiny

## Setup

In Authentik, create a proxy provider for a single application with the URL
`https://scrutiny.nathanv.app`. Ensure you assign the application to an outpost.

## Post launch

Run the metric collection command on all pods once.

```bash
kubectl -n scrutiny get pods -l app=scrutiny-collector -o name | xargs -I {} kubectl exec -n scrutiny {} -- /opt/scrutiny/bin/scrutiny-collector-metrics run
```

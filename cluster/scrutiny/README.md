# Scrutiny

## Post launch

Run the metric collection command on all pods once.

```bash
kubectl -n scrutiny get pods -l app=scrutiny-collector -o name | xargs -I {} kubectl exec -n scrutiny {} -- /opt/scrutiny/bin/scrutiny-collector-metrics run
```

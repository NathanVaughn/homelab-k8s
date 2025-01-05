# Cluster

## Force update

```bash
flux reconcile source git flux-system
flux reconcile kustomization flux-system -n flux-system
```

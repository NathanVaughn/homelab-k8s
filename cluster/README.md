# Cluster

## Force update

```bash
flux reconcile source git flux-system
flux reconcile kustomization flux-system -n flux-system
```

## Troubleshooting

```bash
kubectl get events -n flux-system --field-selector type=Warning
```

```bash
flux logs -n foo
```

If a SealedSecret is getting stuck in `Progressing` state, delete the associated
`Secret` and try the reconciliation again.

## Wipe namespace

```bash
kubectl delete --all pods --namespace=foo
# or
kubectl delete --all deployments --namespace=foo
```

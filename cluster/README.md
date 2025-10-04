# Cluster

## Registry proxy

To prefix the registry proxy `cr.nathanv.app`, the following syntax options can be used:

### Prefix

This requires that the immediately following line is in the format `image: {image name}`.

```yaml
# registry-proxy image-prefix
image: cr.nathanv.app/docker.io/library/busybox:1.37.0
```

### Block

This can be used when proxying the image requires adding additional lines.
When disabled, the block will be commented out.

```yaml
# registry-proxy block-start
outposts:
    container_image_base: cr.nathanv.app/ghcr.io/goauthentik/%(type)s:%(version)s
# registry-proxy block-end
```

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

## Upgrading PostgreSQL Databases

<https://github.com/bitnami/charts/issues/14926#issuecomment-2551470705>

```bash
kubectl exec -it -n $namespace $pod -- bash
pg_dump -U $user $database > /var/lib/postgresql/18/docker/backup.sql

# Upgrade the chart

kubectl exec -it -n $namespace $pod -- bash
psql -U $user -h localhost -f /var/lib/postgresql/18/docker/backup.sql

# Once checked

rm -rf /var/lib/postgresql/18
```

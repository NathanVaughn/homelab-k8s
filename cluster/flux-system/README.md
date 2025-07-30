# Flux

## Upgrading Flux

```bash
flux check --pre
flux install --registry cr.nathanv.app/ghcr.io/fluxcd --export > ./cluster/flux-system/gotk-components.yaml
```

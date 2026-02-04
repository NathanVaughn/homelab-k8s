# Flux

## Upgrading Flux

```bash
flux check --pre
flux install --registry cr.nathanv.app/ghcr.io/fluxcd --export > ./cluster/flux-system/gotk-components.yaml
```

## Failed Helm Release Upgrade

<https://fluxcd.io/flux/components/helm/helmreleases/#forcing-a-release>

<https://fluxcd.io/flux/components/helm/helmreleases/#resetting-remediation-retries>
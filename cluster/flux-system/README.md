# Flux

## Upgrading Flux

<https://github.com/fluxcd/flux2/discussions/5572>

```bash
flux check --pre
flux install --registry cr.nathanv.app/ghcr.io/fluxcd --export > ./cluster/flux-system/gotk-components.yaml
flux migrate
```

## Failed Helm Release Upgrade

<https://fluxcd.io/flux/components/helm/helmreleases/#forcing-a-release>

<https://fluxcd.io/flux/components/helm/helmreleases/#resetting-remediation-retries>
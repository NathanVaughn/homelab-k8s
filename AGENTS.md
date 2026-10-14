# Agent Notes

This repository is automatically reconciled by Flux every 5 minutes. Before
making changes in this repository, suspend the `flux-system` Kustomization:

```sh
flux suspend kustomization flux-system -n flux-system
```

After the changes are complete, resume it:

```sh
flux resume kustomization flux-system -n flux-system
```

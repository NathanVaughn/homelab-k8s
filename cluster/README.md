## Create a helm source

```bash
flux create source helm $NAME --url $HELMURL --namespace $NAME --export
```

## Create a helm release

```bash
flux create helmrelease $RELEASENAME --chart $NAME --source HelmRepository/$NAME --chart-version $VERSION --namespace $NAME --export
```

## Force update

```bash
flux reconcile source git flux-system
```

## Fetch public key

```bash
kubeseal --fetch-cert --controller-namespace=sealed-secrets > sealed-secrets-public-key.pem
```

## Forward a port

```bash
kubectl port-forward service/$NAME $PORT
```

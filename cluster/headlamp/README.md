# Headlamp

## Setup

You'll need to setup OIDC login in the K8S API.

In Authentik, configure a OAuth2 provider. Use the redirect URL as
`http://localhost:8000`

```bash
export CLIENT_ID=$CLIENT_ID
export CLIENT_SECRET=$CLIENT_SECRET
# setup oidc-login
kubectl oidc-login setup --oidc-issuer-url=https://authentik.nathanv.app/application/o/k8s-oidc/ --oidc-client-id=$CLIENT_ID --oidc-client-secret=$CLIENT_SECRET
# create oidc user
kubectl config set-credentials authentik-oidc --exec-api-version=client.authentication.k8s.io/v1beta1 --exec-command=kubectl --exec-arg=oidc-login --exec-arg=get-token --exec-arg=--oidc-issuer-url=https://authentik.nathanv.app/application/o/k8s-oidc/ --exec-arg=--oidc-client-id=$CLIENT_ID --exec-arg=--oidc-client-secret=$CLIENT_SECRET --exec-arg=--oidc-extra-scope=email,profile
# link user
kubectl config set-context authentik-oidc --namespace=default --cluster=authentik --user=authentik-oidc
```

Test with the following:

```bash
kubectl config use-context authentik-oidc
kubectl get ns
kubectl config set-context default
```


Finally, set up the secrets. In Authentik, configure a OAuth2 provider.
Use the redirect URL as `https://headlamp.nathanv.app/oidc-callback`

```bash
export HEADLAMP_CONFIG_OIDC_CLIENT_ID=$HEADLAMP_CONFIG_OIDC_CLIENT_ID
export HEADLAMP_CONFIG_OIDC_CLIENT_SECRET=$HEADLAMP_CONFIG_OIDC_CLIENT_SECRET
kubectl apply -f namespace.yaml
kubectl -n headlamp create secret generic headlamp-secrets --from-literal=config.oidc.clientID=$HEADLAMP_CONFIG_OIDC_CLIENT_ID --from-literal=config.oidc.clientSecret=$HEADLAMP_CONFIG_OIDC_CLIENT_SECRET --dry-run=client -o yaml > secret.yaml
kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
```

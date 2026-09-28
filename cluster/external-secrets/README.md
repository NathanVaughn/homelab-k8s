# External Secrets

[External Secrets Operator](https://external-secrets.io/) (ESO) syncs secrets from
[Bitwarden Secrets Manager](https://bitwarden.com/products/secrets-manager/) into
Kubernetes `Secret` resources, replacing per-app `SealedSecret` manifests.

Bitwarden org: `9c0ec910-6f86-4fdc-9334-af9201083c7b`
Bitwarden project ("Homelab"): `b4f1f377-ed70-4637-9df9-b4d200f08a92`

## Regenerating the SDK server TLS certificate

If the certificate ever needs to be rotated (it's valid for 10 years):

```bash
openssl req -x509 -newkey rsa:2048 -sha256 -days 3650 -nodes \
  -keyout tls.key -out tls.crt -subj "/O=external-secrets.io/CN=bitwarden-sdk-server" \
  -addext "subjectAltName=DNS:bitwarden-sdk-server.external-secrets.svc.cluster.local,DNS:bitwarden-sdk-server,DNS:localhost,IP:127.0.0.1" \
  -addext "basicConstraints=critical,CA:TRUE" \
  -addext "keyUsage=critical,digitalSignature,keyCertSign,keyEncipherment"

kubectl create secret tls bitwarden-tls-certs -n external-secrets \
  --cert=tls.crt --key=tls.key --dry-run=client -o yaml > secret.yaml

kubectl patch --local -f secret.yaml --type=json \
  -p '[{"op":"add","path":"/data/ca.crt","value":"'"$(base64 -w0 tls.crt)"'"}]' \
  -o yaml > secret-with-ca.yaml

kubeseal --cert=../sealed-secrets/sealed-secrets-public-key.pem --format=yaml \
  < secret-with-ca.yaml > sealed-secret-bitwarden-tls-certs.yaml
```

## Setting/rotating the Bitwarden machine account access token

1. Create (or rotate) a **machine account** in Bitwarden Secrets Manager with
   read (or read-write, for PushSecret) access to the `Homelab` project.
2. Run the following **locally in a terminal**, substituting your real access
   token.

   ```bash
   kubectl create secret generic bitwarden-access-token \
     --namespace=external-secrets \
     --from-literal=token='<YOUR_BITWARDEN_MACHINE_ACCOUNT_ACCESS_TOKEN>' \
     --dry-run=client -o yaml \
     | kubeseal --cert=../sealed-secrets/sealed-secrets-public-key.pem --format=yaml \
     > sealed-secret-bitwarden-access-token.yaml
   ```

3. Commit the resulting `sealed-secret-bitwarden-access-token.yaml` (it only
   contains ciphertext).

## Using it in an app

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: myapp-env
  namespace: myapp
spec:
  refreshInterval: 1h0m0s
  secretStoreRef:
    name: bitwarden-secretsmanager
    kind: ClusterSecretStore
  target:
    name: myapp-env
  data:
    - secretKey: MYAPP_DB_PASSWORD
      remoteRef:
        key: MYAPP_DB_PASSWORD
```

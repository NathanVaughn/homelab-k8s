# Longhorn

## Setup

In Authentik, create a proxy provider for a single application with the URL
`https://longhorn.nathanv.app`. Ensure you assign the application to an outpost.

```bash
export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
export AWS_ENDPOINTS=$S3_ENDPOINT
export VIRTUAL_HOSTED_STYLE=false
# change dollar sign variables above this line
kubectl apply -f namespace.yaml

kubectl -n longhorn create secret generic longhorn-env \
--from-literal=AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
--from-literal=AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
--from-literal=AWS_ENDPOINTS=$AWS_ENDPOINTS \
--from-literal=VIRTUAL_HOSTED_STYLE=$VIRTUAL_HOSTED_STYLE \
--dry-run=client -o yaml > secret.yaml

kubeseal --format=yaml --cert=../sealed-secrets/sealed-secrets-public-key.pem < secret.yaml > sealed-secret.yaml
# optional
kubectl apply -f sealed-secret.yaml
kubectl delete secret -n longhorn longhorn-env
```

## Post Setup

In the web UI, manually modify the reserved storage space for each node.
20 GB tends to work well.

All persistent volume claims should use the storage class name "longhorn".
This is a ReadWriteOnce storage class which means that only one node can
access the volume for writing at a time.

Volumes which needed to *modified* by multiple pods at the same time should use the
storage class "longhorn-rwx".

### Accessing a Volume

1. Use the Longhorn UI to figure out what node the volume is on.
2. SSH into the node.
3. Run `sudo lsblk` to find the mount path. In the form of `/var/lib/kubelet/pods/{pod-guid}/volumes/kubernetes.io~csi/pvc-{vol-guid}/mount`
4. `sudo -s`
5. `cd /var/lib/kubelet/pods/{pod-guid}/volumes/kubernetes.io~csi/pvc-{vol-guid}/mount`

Alternatively, you can connect a shell to a pod and modify the volume from there:

```bash
kubectl get pods -n {namespace}
# find your pod
kubectl exec -n {namespace} -it {pod-name} -- /bin/bash
```

This tends to be easier.

### Manually Run Backup Job

```bash
kubectl create job --from=cronjob/nightly-backup nightly-backup-oneshot -n longhorn
```

Check when it's done with

```bash
kubectl get jobs -n longhorn nightly-backup-oneshot
```

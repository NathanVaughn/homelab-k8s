Setup a backup target in the Longhorn UI under Settings.

All persistent volume claims should use the storage class name "longhorn".

Set the longhorn storage class as default:

```bash
# set local-path to not default
kubectl patch storageclass local-path -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"false"}}}'
# set longhorn to default
kubectl patch storageclass longhorn -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```
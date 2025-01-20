# kube-vip

## Post Setup

`externalTrafficPolicy` MUST be `Cluster` on services for things to work correctly.
This however will mask source IP addresses.

```yaml
externalTrafficPolicy: Cluster
```

This is the default selection.

## Issues

kube-vip may interfere with attaching shells to pods.

Temporarily change the IP address directly to a node in the kube config
to work around this.

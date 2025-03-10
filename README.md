# Homelab K8s

This repository is for my homelab, utilizing Kubernetes.

The [devcontainer](https://containers.dev) should be used for all development.

## Folder Structure

### cluster

This folder contains Kubernetes manifests synced with [flux](https://fluxcd.io/).
Individual folders have specific instructions for any manual actions
needed like setting up secrets.

### os

Script and information to setup node operating systems.

### scripts

Scripts for cluster management. Outside the `cluster` directory to not annoy
`flux`.

### software

This uses [pyinfra](https://pyinfra.com/) to deploy [k3s](https://k3s.io/)
and other operating system settings and packages.

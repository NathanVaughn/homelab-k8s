# Homelab K8s

This repository is for my homelab, utilizing Kubernetes.

The [devcontainer](https://containers.dev) should be used for all development.

## Folder Structure

### cluster

This folder contains Kubernetes manifests synced with [flux](https://fluxcd.io/).
Individual folders have specific instructions for any manual actions
needed like setting up secrets.

### docs

Some additional documentation.

### os

Script and information to setup node operating systems.

### software

This uses [pyinfra](https://pyinfra.com/) to deploy [k3s](https://k3s.io/)
and other operating system settings and packages.

# Homelab K8s
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FNathanVaughn%2Fhomelab-k8s.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FNathanVaughn%2Fhomelab-k8s?ref=badge_shield)


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

### deployment

This uses [pyinfra](https://pyinfra.com/) to deploy [k3s](https://k3s.io/)
and other operating system settings and packages.


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FNathanVaughn%2Fhomelab-k8s.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FNathanVaughn%2Fhomelab-k8s?ref=badge_large)
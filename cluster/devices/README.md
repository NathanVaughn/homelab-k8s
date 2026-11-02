# IP Addresses

## Overview

10.0.0.1/20

| Description          | Value                  |
| -------------------- | ---------------------- |
| Gateway IP           | 10.0.0.1               |
| Network Broadcast IP | 10.0.15.255            |
| Network IP Count     | 4094                   |
| Network IP Range     | 10.0.0.1 - 10.0.15.254 |
| Network Subnet Mask  | 255.255.240.0          |

### DHCP Pool

10.0.0.30 - 10.0.0.254

### Static IP Addresses

Layout: `.2-.9` infrastructure, `.10-.19` Kubernetes nodes, `.20-.29` other
static devices, `.30+` DHCP.

| Device               | IP        | Description                       |
| -------------------- | --------- | --------------------------------- |
| butch.nathanv.home   | 10.0.0.2  | DNS Server and Network Controller |
| billy.nathanv.home   | 10.0.0.10 | Kubernetes node 1                 |
| jesse.nathanv.home   | 10.0.0.11 | Kubernetes node 2                 |
| tom.nathanv.home     | 10.0.0.12 | Kubernetes node 3                 |
| annie.nathanv.home   | 10.0.0.13 | Kubernetes node 4                 |
| will.nathanv.home    | 10.0.0.14 | Kubernetes node 5                 |
| cassidy.nathanv.home | 10.0.0.20 | 3D print server                   |

### Load Balancer Addresses

| Service                 | IP          | DNS                                |
| ----------------------- | ----------- | ---------------------------------- |
| control plane           | 10.10.10.1  | k8s-control-plane.svc.nathanv.home |
| traefik (reverse proxy) | 10.10.10.2  | reverse-proxy.svc.nathanv.home     |
| chrony (NTP)            | 10.10.10.3  | ntp.svc.nathanv.home               |
| Omada                   | 10.10.10.4  | omada.svc.nathanv.home             |
| technitium (DNS)        | 10.10.10.10 | dns.svc.nathanv.home               |

The kube-vip pool for other services is 10.10.10.100 - 10.10.10.250. The gateway must route 10.10.10.0/24.

k3s reserves 10.42.0.0/16 (pods) and 10.43.0.0/16 (services); do not use them.

## IoT Network

VLAN 10

10.20.0.1/24

| Description          | Value                   |
| -------------------- | ----------------------- |
| Gateway IP           | 10.20.0.1               |
| Network Broadcast IP | 10.20.0.255             |
| Network IP Count     | 254                     |
| Network IP Range     | 10.20.0.1 - 10.20.0.254 |
| Network Subnet Mask  | 255.255.255.0           |

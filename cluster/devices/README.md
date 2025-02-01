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

| Device               | IP        | Description                       |
| -------------------- | --------- | --------------------------------- |
| butch.nathanv.home   | 10.0.0.2  | DNS Server and Network Controller |
| tex.nathanv.home     | 10.0.0.10 | Old app server                    |
| cassidy.nathanv.home | 10.0.0.11 | 3D print server                   |
| billy.nathanv.home   | 10.0.0.20 | Kubernetes node 1                 |
| jesse.nathanv.home   | 10.0.0.21 | Kubernetes node 2                 |
| tom.nathanv.home     | 10.0.0.22 | Kubernetes node 3                 |
| annie.nathanv.home   | 10.0.0.23 | Kubernetes node 4                 |
| will.nathanv.home    | 10.0.0.24 | Kubernetes node 5                 |

### Load Balancer Addresses

| Service                 | IP       | DNS                                |
| ----------------------- | -------- | ---------------------------------- |
| control plane           | 10.0.1.1 | k8s-control-plane.svc.nathanv.home |
| traefik (reverse proxy) | 10.0.1.2 | reverse-proxy.svc.nathanv.home     |
| chrony (NTP)            | 10.0.1.3 | ntp.svc.nathanv.home               |
| technitium (DNS)        | 10.0.1.4 | dns.svc.nathanv.home               |
| Factorio                | 10.0.1.5 | factorio.svc.nathanv.home          |
| Omada                   | 10.0.1.6 | omada.svc.nathanv.home             |

## IoT Network

VLAN 10

10.10.0.1/24

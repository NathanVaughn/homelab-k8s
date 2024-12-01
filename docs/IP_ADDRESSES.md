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

## DHCP Pool

10.0.0.30 - 10.0.0.254

## Static IP Addresses

| Device                | IP        | Description                       |
| --------------------- | --------- | --------------------------------- |
| ares.nathanv.home     | 10.0.0.5  | DNS Server and Network Controller |
| zeus.nathanv.home     | 10.0.0.10 | Main app server                   |
| poseidon.nathanv.home | 10.0.0.11 | 3D print server                   |
| retropie.nathanv.home | 10.0.0.12 | Retropie                          |
| apollo.nathanv.home   | 10.0.0.13 | Laptop                            |
| billy.nathanv.home    | 10.0.0.20 | Kubernetes node 1                 |
| jesse.nathanv.home    | 10.0.0.21 | Kubernetes node 2                 |
| tom.nathanv.home      | 10.0.0.22 | Kubernetes node 3                 |
| annie.nathanv.home    | 10.0.0.23 | Kubernetes node 4                 |

## Load Balancer Addresses

| Service       | IP       |
| ------------- | -------- |
| control plane | 10.0.1.1 |
| traefik       | 10.0.1.2 |
| ntp           | 10.0.1.3 |

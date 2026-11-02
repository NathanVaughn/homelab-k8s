# Omada

## Setup

In Authentik, create a proxy provider for a single application with the URL
`https://omada.nathanv.app`. Ensure you assign the application to an outpost.

## Post Setup

### DHCP Reservations

Configured under Site -> Network Config -> Transmission -> DHCP Reservation.

### DHCP Settings

Configured under Site -> Network Config -> Network Settings -> LAN.

Default VLAN:

VLAN ID: 1
Set the IP address and mask to `10.0.0.1/20`.
Set the DHCP pool range to `10.0.0.30 - 10.0.15.254`.

IOT VLAN:

VLAN ID: 10
Set the IP address and mask to `10.20.0.1/24`.
Set the DHCP pool range to `10.20.0.1-10.20.0.254`.

NTP is option 42 under the Advanced DHCP Options.

### Static Route for Service VIPs

The kube-vip LoadBalancer addresses live in `10.10.10.0/24`, which is not a
configured LAN. kube-vip answers ARP for them from whichever node holds the
VIP, so the gateway must treat that subnet as directly reachable on the
default LAN rather than via a fixed node IP.

Configured under Site -> Network Config -> Transmission -> Routing -> Static Routing.

Create a route with:

| Field       | Value           |
| ----------- | --------------- |
| Name        | `service-vips`  |
| Status      | Enabled         |
| Destination | `10.10.10.0/24` |
| Route Type  | Interface       |
| Interface   | Default         |
| Metric      | `1`             |

Verify from a LAN client:

```sh
ping 10.10.10.10
dig @10.10.10.10 example.com
```

Traffic from LAN clients to the VIPs passes through the gateway and returns
via the same interface. If a firewall/ACL rule blocks LAN -> LAN traffic,
allow `10.0.0.0/20` -> `10.10.10.0/24`.

### Mesh Settings

Configured under Site -> Network Config -> Site Settings.

Enable Mesh and Band Steering under Wireless Features.

### Deep Packet Inspection

Configured under Site -> Network Config -> Security -> Application Control.

Enable Deep Packet Inspection and Logging Traffic.

### Block Google DNS

This helps for things like Chromecasts that like to ignore DHCP DNS.

First, create an IP group. This is under Site -> Network Config -> Profiles -> Groups.
This should include 8.8.8.8/32 and 8.8.4.4/32.

Now, go under Site -> Network Config -> Security -> ACL.
Create a rule for the gateway blocking traffic from LAN -> WAN, for the Google DNS
IP group.

!!! Amazon Prime Video does not work with this rule enabled. Temporarily disable
when starting to stream a movie/show.

### APs

Optionally, enable OFDMA for both APs under Site -> Devices -> {AP} -> Manage Device -> Config -> Wireless.

### Lock AP

Select my desktop under clients. Lock to Primary AP. Otherwise it seems to switch
to the Garage AP at the worst possible moments.

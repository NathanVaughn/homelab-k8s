# Omada

## Setup

In Authentik, create a proxy provider for a single application with the URL
`https://omada.nathanv.app`. Ensure you assign the application to an outpost.

## Post Setup

### DHCP Reservations

Configured under Site Settings -> Services -> DHCP Reservation.

### DHCP Settings

Configured under Site Settings -> Wired Networks -> LAN -> Networks -> Default -> Networks.

NTP is option 42 under the Advanced DHCP Options.

### Mesh Settings

Configured under Site Settings -> Site.

Enable Mesh and Band Steering under Wireless Features.

### Deep Packet Inspection

Configured under Site Settings -> Network Security -> Application Control.

Enable Deep Packet Inspection and Logging Traffic.

### Block Google DNS

This helps for things like Chromecasts that like to ignore DHCP DNS.

First, create an IP group. This is under Site Settings -> Profiles -> Groups.
This should include 8.8.8.8 and 8.8.4.4.

Now, go under Site Settings -> Network Security -> ACL.
Create a rule for the gateway blocking traffic from LAN -> WAN, for the Google DNS
IP group.

!!! Amazon Prime Video does not work with this rule enabled. Temporarily disable
when starting to stream a movie/show.

### APs

Optionally, enable OFDMA for both APs under Advanced.

### Lock AP

Select my desktop under clients. Lock to Primary AP. Otherwise it seems to switch
to the Garage AP at the worst possible moments.

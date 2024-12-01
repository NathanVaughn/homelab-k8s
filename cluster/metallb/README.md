# MetalLB

## Setup

Make sure the IP address range used is within the local network's subnet.
Using something outside that will not work with device's routing table.

Also make sure the IP address range is outside the DHCP range of the router.
An easy method is to make the gateway/subnet range be a /23 to /20,
and then the DHCP range a /24 within that range.

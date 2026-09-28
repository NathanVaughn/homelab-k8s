# ADS-B

## Setup

In Authentik, create a proxy provider for a single application with the URL
`https://readsb.nathanv.app`. Ensure you assign the application to an outpost.

`TZ` is non-secret configuration in [configmap.yaml](configmap.yaml), shared by
the deployments.

## Bitwarden secrets

- `ADSB_FLIGHTAWARE_FEEDER_ID`
- `ADSB_FLIGHTRADAR24_KEY`
- `ADSB_PLANEFINDER_SHARECODE`
- `ADSB_LAT`
- `ADSB_LON`
- `ADSB_ALT`

## Discussion

These Docker containers don't follow semver, so Renovate struggles updating them.
Instead, I use hash pinning.

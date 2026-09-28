# Omada Exporter

Not using Helm chart because of <https://github.com/charlie-haley/charts/pull/11>
and <https://github.com/charlie-haley/omada_exporter/issues/101>.

## Setup

In the Omada controller, create a user called `prometheus` as a Viewer.

Additionally, go to Settings -> Platform Integration, and create an OpenAPI app.
Use the "client" mode, and give it viewer permissions.

## Bitwarden secrets

- `OMADA_EXPORTER_CLIENT_ID`
- `OMADA_EXPORTER_PASSWORD`
- `OMADA_EXPORTER_SECRET_ID`
- `OMADA_EXPORTER_USERNAME`

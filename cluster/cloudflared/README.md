# Cloudflared

## Setup

First, you can run `create-config.py` to generate the configuration file.
This creates a config for services with an external DNS record set.

[Install `cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).

```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
rm cloudflared-linux-amd64.deb
```

Now, login and create the tunnel:

```bash
cloudflared tunnel login
cloudflared tunnel create k8s-tunnel
cp ~/.cloudflared/*.json tunnel.json
cloudflared tunnel route dns k8s-tunnel tunnel.nathanv.app
```

## Bitwarden secrets

- `CLOUDFLARED_CREDENTIALS_FILE` (the tunnel credentials JSON)

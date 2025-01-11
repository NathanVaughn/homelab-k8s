FROM ghcr.io/nathanvaughn/devcontainers/python:latest
RUN sudo apt-get update -y \
 && sudo apt-get install whois openssh-client -y
# install kubelogin
RUN cd $(mktemp -d) \
 && curl -fsSLO https://github.com/int128/kubelogin/releases/download/v1.31.1/kubelogin_linux_amd64.zip \
 && unzip kubelogin_linux_amd64.zip \
 && mkdir -p ~/.local/bin/ \
 && mv kubelogin ~/.local/bin/kubectl-oidc_login \
 && rm -rf ./*

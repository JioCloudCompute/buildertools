#!/bin/bash
source /etc/environment
cd /usr/local/bin
wget -e use_proxy=yes -e https_proxy=$http_proxy https://releases.hashicorp.com/consul-template/0.12.0/consul-template_0.12.0_linux_amd64.zip
unzip *.zip
rm *.zip

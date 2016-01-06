#!/bin/bash
source /etc/environment
cd /usr/local/bin
wget -e use_proxy=yes -e https_proxy=$http_proxy https://dl.bintray.com/mitchellh/consul/0.3.0_linux_amd64.zip
unzip *.zip
rm *.zip

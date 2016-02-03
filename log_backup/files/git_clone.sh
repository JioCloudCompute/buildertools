#!/bin/bash
source /etc/environment
export git_protocol="https"

#wget -O /tmp/google.com.html google.com
git config --global http.proxy $http_proxy
git config --global https.proxy $https_proxy
git clone $1 $2

git config --global --unset http.proxy
git config --global --unset https.proxy


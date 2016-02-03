#!/bin/bash
source /etc/environment
cd /tmp
wget  -e use_proxy=yes -e https_proxy=$http_proxy https://collectd.org/files/collectd-5.5.0.tar.bz2
tar jxf collectd-5.5.0.tar.bz2
cd collectd-5.5.0/
sudo ./configure
sudo make all install

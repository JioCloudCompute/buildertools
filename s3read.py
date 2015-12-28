#!/bin/bash
filename=$1
IFS=$'\n'
mkdir -p /etc/conf/ansible-vars/files
mkdir -p /etc/conf/ansible-vars/group_vars
mkdir -p /etc/conf/ansible-vars/certs
mkdir -p certs
mkdir -p group_vars
for next in `cat $filename`
do
     touch /etc/conf/ansible-vars/$next
     python /home/compute_team/deployment-code/AWSS3ConfigManager/configManager/apply_changes.py /home/compute_team/deployment-code/AWSS3ConfigManager/config-manager-config.conf ansible-vars/$next
     ln -s /etc/conf/ansible-vars/$next $next
done
exit 0

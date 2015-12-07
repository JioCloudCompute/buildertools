#!/bin/bash
#
# Parallel provisioning for vagrant
#
up() {
  vagrant up --no-provision
}

provision() {
  sleep 5
  . newtokens.sh
  if [ ! -n $consul_discovery_token ]; then
    echo "Error fetching consul discovery token, exiting"
    exit 100
  fi
  for i in `vagrant status | grep running | awk '{print $1}'`; do 
    vagrant provision $i &
  done
}

destroy() {
  vagrant destroy -f
}

case $1 in
  'destroy')
    destroy
    ;;
  'up')
    up
    provision
    ;;
  'provision')
    provision
    ;;
  'reset')
    destroy
    up
    provision
    ;;
  *)
    echo "Invalid operation. Valid operations are destroy, up, provision,reset"
    exit 100
    ;;
esac

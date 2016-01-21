#sed -i 's/vpramo/vpcjiocloud/g' `grep /etc/apt/* vpramo -r -l`
#sed -i 's/\(deb.*jiocloud.rustedhalo.com\)/#\1/g' `grep 'jiocloud.rustedhalo.com' /etc/apt/* -r -l`
apt-get update
apt-get purge -f --yes puppet-vpc
apt-get install -f --force-yes --yes puppet-vpc
puppet apply /etc/puppet/manifests/site.pp


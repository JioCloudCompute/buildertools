# -*- mode: ruby -*-
# vi: set ft=ruby :
require 'yaml'

Vagrant.configure("2") do |config|

  default_flavor = 'small'
  default_image = 'trusty'

  # allow users to set their own environment
  # which effect the hiera hierarchy and the
  # cloud file that is used
  environment = ENV['env'] || 'vagrant-vbox'
  layout = ENV['layout'] || 'compute_arch'
  map = ENV['map'] || environment

  config.vm.provider :virtualbox do |vb, override|
#    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end

  config.vm.provider "lxc" do |v, override|
    override.vm.box = "fgrehm/trusty64-lxc"
  end

  last_octet = 41
  env_data = YAML.load_file("environment/#{layout}.yaml")

  map_data = YAML.load_file("environment/#{map}.map.yaml")

  machines = {}
  env_data['resources'].each do |name, info|
    (1..info['number']).to_a.each do |idx|
      machines["#{name}#{idx}"] = info
    end
  end

  machines.each do |node_name, info|

    config.vm.define(node_name) do |config|

      config.vm.provider :virtualbox do |vb, override|
        image = info['image'] || default_image
        override.vm.box = map_data['image']['virtualbox'][image]

        flavor = info['flavor'] || default_flavor
        vb.memory = map_data['flavor'][flavor]['ram']
        vb.cpus = map_data['flavor'][flavor]['cpu']
      end

 #     config.vm.synced_folder("hiera/", '/etc/puppet/hiera/')
 #     config.vm.synced_folder("modules/", '/etc/puppet/modules/')
 #     config.vm.synced_folder("manifests/", '/etc/puppet/modules/rjil/manifests/')
 #     config.vm.synced_folder("files/", '/etc/puppet/modules/rjil/files/')
 #     config.vm.synced_folder("templates/", '/etc/puppet/modules/rjil/templates/')
 #     config.vm.synced_folder("lib/", '/etc/puppet/modules/rjil/lib/')
 #     config.vm.synced_folder(".", "/etc/puppet/manifests")

      # This seems wrong - Soren

      config.vm.host_name = "#{node_name}.domain.name"

      if ENV['http_proxy']
        config.vm.provision 'shell', :inline =>
        "echo \"Acquire::http { Proxy \\\"#{ENV['http_proxy']}\\\" }\" > /etc/apt/apt.conf.d/03proxy"
        config.vm.provision 'shell', :inline =>
        "echo http_proxy=#{ENV['http_proxy']} >> /etc/environment"
      end


      if ENV['https_proxy']
        config.vm.provision 'shell', :inline =>
        "echo https_proxy=#{ENV['https_proxy']} >> /etc/environment"
        config.vm.provision 'shell', :inline =>
        "echo no_proxy='127.0.0.1,169.254.169.254,localhost,consul,jiocloud.com' >> /etc/environment"
      end

      # upgrade puppet

 
      net_prefix = ENV['NET_PREFIX'] || "192.168.100.0"
      config.vm.network "private_network", :type => :dhcp, :ip => net_prefix, :netmask => "255.255.255.0", :adapter => 2
     config.vm.provision "ansible" do |ansible|
     ansible.playbook = "test.yml"
     ansible.sudo = true
    end
    end 
  end
end

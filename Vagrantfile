# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/trusty64"

    config.vm.network :forwarded_port, guest: 80, host: 8000  # nginx
    config.vm.network :forwarded_port, guest: 8000, host: 8001  # local
    config.vm.network :forwarded_port, guest: 8888, host: 8888  # jasmine
    config.vm.network :forwarded_port, guest: 5432, host: 5432  # postgres
    config.vm.hostname = "lile-dev"
    config.vm.network :private_network, ip: "192.168.13.40"


    config.vm.synced_folder "salt/roots/", "/srv/salt/"


    config.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", 1024]
    end

    config.vm.provision :salt do |salt|
        salt.minion_config = "salt/minion"
        salt.run_highstate = true
        salt.bootstrap_options = "-F -c /tmp/ -P"
    end
end
  
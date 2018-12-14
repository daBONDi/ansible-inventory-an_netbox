# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|

  config.vm.define "netbox" do | nb |
    nb.vm.box = "ubuntu/xenial64"
    nb.vm.hostname = "netbox-demo"
    nb.vm.network "private_network", ip: "192.168.99.20"
    nb.vm.network :forwarded_port, guest: 80, host: 8080, id: 'http'
    nb.vm.synced_folder "./vagrant/netbox/config_files", "/vagrant"
    nb.vm.provider :virtualbox do |vb|
      vb.name = "Netbox-Demo"
      vb.memory = 2048
      vb.cpus = 1
      vb.customize ["modifyvm", :id, "--ostype", "Ubuntu_64"]
    end
  
    nb.vm.provision :shell, path: "vagrant/netbox/bootstrap.sh"
  end 

  config.vm.define "ansible" do | ansible |
    ansible.vm.box = "ubuntu/xenial64"
    ansible.vm.hostname = "ansible"
    ansible.vm.network "private_network", ip: "192.168.99.10"

    ansible.vm.provider :virtualbox do |vb|
      vb.name = "Ansible"
      vb.memory = 2048
      vb.cpus = 1
      vb.customize ["modifyvm", :id, "--ostype", "Ubuntu_64"]
    end

    ansible.vm.provision "ansible_local" do | ansible |
      ansible.install_mode = "pip"
      ansible.playbook = "vagrant/ansible/config-ansible-server.yml"
      ansible.become = true
    end

    ansible.vm.synced_folder "./ansible", "/opt/it-infra", id: "it-infra", owner: "vagrant", group: "www-data", mount_options: ["dmode=775","fmode=664"]


  end 

end

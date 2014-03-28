# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "arch"
  config.vm.box_url = "https://dl.dropboxusercontent.com/u/6750592/Arch_Linux_2013.11_x64.box"
  config.vm.synced_folder ".", "/rpi"
  #config.vm.hostname = "rpi"
  #config.vm.network "private_network", ip: "10.0.2.15"


  config.vm.provider "virtualbox" do |vb|
     vb.customize ["modifyvm", :id, "--memory", "512"]
  end

  config.vm.provision "shell", inline: "if [ -z `which python2` ]; then sudo pacman -Sy --noconfirm python2; fi"

  config.vm.provision "ansible" do |ansible|
      ansible.sudo = "yes"
      ansible.limit = "all"
      #ansible.verbose = "vvvv"
      ansible.host_key_checking = "false"
      ansible.playbook = "ansible/site.yml"
      ansible.extra_vars = {ansible_python_interpreter: "/usr/bin/python2"}
  end
end

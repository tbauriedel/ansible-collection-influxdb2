# -*- mode: ruby -*-
# vi: set ft=ruby :
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.define "ubuntu" do |ubuntu|
    ubuntu.vm.hostname = "influxdb-ubuntu"
    ubuntu.vm.box = "bento/ubuntu-22.04"
    ubuntu.vm.provision "ansible" do |ansible|
      ansible.playbook = "vagrant-tests.yml"
    end
  end

  config.vm.define "centos" do |centos|
    centos.vm.hostname = "influxdb-centos"
    centos.vm.box = "eurolinux-vagrant/centos-stream-9"
    centos.vm.provision "ansible" do |ansible|
      ansible.playbook = "vagrant-tests.yml"
    end
  end
end
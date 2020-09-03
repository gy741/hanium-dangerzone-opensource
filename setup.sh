#!/bin/bash

#echo 'ubuntu:korea123!!' | chpasswd
sudo -S sh -c 'echo "ubuntu:korea123!!" | chpasswd'

echo "deb https://packagecloud.io/firstlookmedia/code/ubuntu/ bionic main" | sudo tee -a /etc/apt/sources.list.d/firstlookmedia_code.list
curl -L https://packagecloud.io/firstlookmedia/code/gpgkey | sudo apt-key add -

sudo apt-get update
# sudo apt-get install -y ubuntu-desktop xrdp curl gnupg apt-transport-https dangerzone python3 python3-pip
sudo apt-get install -y curl gnupg apt-transport-https dangerzone python3 python3-pip

pip3 install django>=2.0
mkdir -p /tmp/dangerzone-pixel
mkdir -p /tmp/dangerzone-safe

sudo usermod -aG docker ubuntu
sudo chmod 666 /var/run/docker.sock
sudo systemctl daemon-reload
sudo systemctl start docker
sudo systemctl enable docker
/usr/bin/docker pull flmcode/dangerzone

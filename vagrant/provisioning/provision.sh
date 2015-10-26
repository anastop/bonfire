#!/usr/bin/env bash

apt-get update

apt-get install -y git-core git vim cmake unzip make automake curl \
                   build-essential g++-4.8 m4 pkg-config libtool \
                   firefox xfce4 xfce4-terminal openssh-server python-dev \
                   python-setuptools unzip wget openssh-client


apt-get install -y linux-tools-`uname -r`

wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
python get-pip.py

PIP_LOCATION=`locate pip2.7 | tail -1`
ln -sf $PIP_LOCATION /usr/local/lib/pip2


pip2 install bottle
pip2 install requests
pip2 install requests --upgrade
pip2 install paramiko


chmod -R 777 /opt/
chown -R vagrant.vagrant /opt/

chmod -R 777 /home/vagrant/
chown -R vagrant.vagrant /home/vagrant/

mkdir -p /vagrant/files/
chmod -R 777 /vagrant/files/
chown -R vagrant.vagrant /vagrant/files/

echo "export HOME=/home/vagrant" >> /etc/profile
echo "export HOME=/home/vagrant" >> /etc/bash.bashrc

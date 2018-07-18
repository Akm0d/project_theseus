#!/bin/bash
# This script will save backups of system config files and then link the ones from this project to the correct locations

# Verify root privileges
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

echo "Checking for project dependencies"
for dep in i2cdetect nginx python3 radvd tmux; do
    which $dep  || exit 2
done
echo "Success!"

echo "Setting up Locale"
echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
locale-gen

echo "Setting up ipv6 service"
ln -s $PWD/system/ipv6.sh /usr/local/bin/ipv6.sh 2> /dev/null
ln -s $PWD/system/ipv6.service /etc/systemd/system/ipv6.service 2> /dev/null
ln -s $PWD/system/ipv6.timer /etc/systemd/system/ipv6.timer 2> /dev/null
mkdir -p /etc/systemd/system/timers.target.wants
ln -s $PWD/sytem/ipv6.timer /etc/systemd/system/timers.target.wants/ipv6.timer 2> /dev/null
/usr/local/bin/ipv6.sh

echo "Setting up radvd"
if [ ! -f /etc/radvd.conf.bak ]; then
    mv /etc/radvd.conf /etc/radvd.conf.bak
fi
ln -s $PWD/system/radvd.conf /etc/radvd.conf 2> /dev/null
systemctl restart radvd

echo "Setting up theseus service"
mkdir -p /etc/systemd/system/multi-user.target.wants
ln -s $PWD/system/theseus.service /etc/systemd/system/multi-user.target.wants 2> /dev/null
ln -s $PWD/system/theseus.service /usr/lib/systemd/system/theseus.service 2> /dev/null

echo "Setting up nginx"
if [ ! -f /etc/nginx/nginx.conf.bak ]
    mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
fi
ln -s $PWD/system/nginx.conf /etc/nginx/nginx.conf 2> /dev/null
systemctl restart nginx
systemctl status nginx

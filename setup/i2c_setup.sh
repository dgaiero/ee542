#!/bin/bash
# From: http://www.uugear.com/portfolio/a-single-script-to-setup-i2c-on-your-raspberry-pi/
# file: setup_i2c.sh
#
# This script will enable I2C and install i2c-tools on your Raspberry Pi
#

# check if sudo is used
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# enable I2C on Raspberry Pi
echo '>>> Enable I2C'
if grep -q 'i2c-bcm2708' /etc/modules; then
   echo 'i2c-bcm2708 module already exists, skipping'
else
   echo 'i2c-bcm2708' >>/etc/modules
fi
if grep -q 'i2c-dev' /etc/modules; then
   echo 'i2c-dev module already exists, skipping'
else
   echo 'i2c-dev' >>/etc/modules
fi
if grep -q 'dtparam=i2c1=on' /boot/config.txt; then
   echo 'i2c1 parameter already set, skipping'
else
   echo 'dtparam=i2c1=on' >>/boot/config.txt
fi
if grep -q 'dtparam=i2c_arm=on' /boot/config.txt; then
   echo 'i2c_arm parameter already set, skipping'
else
   echo 'dtparam=i2c_arm=on' >>/boot/config.txt
fi
if [ -f /etc/modprobe.d/raspi-blacklist.conf ]; then
   sed -i 's/^blacklist spi-bcm2708/#blacklist spi-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
   sed -i 's/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
else
   echo 'raspi-blacklist.conf does not exist, skipping'
fi

# install i2c-tools
echo '>>> Install i2c-tools'
if hash i2cget 2>/dev/null; then
   echo 'i2c-tools is installed already, skipping'
else
   apt install -y i2c-tools &&> ../install.log
fi

# Add current account to i 2c group
sudo adduser $USER i2c &&> ../install.log

# Setup spi
if grep -q 'dtparam=spi=on' /boot/config.txt; then
   echo 'spi parameter already set, skipping'
else
   echo 'dtparam=spi=on' >>/boot/config.txt
fi

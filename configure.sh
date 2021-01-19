#!/bin/bash

printf "==========\nTBD rpi setup script\n==========\n"
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

printf "Setting timezone\n"
sudo timedatectl set-timezone America/Los_Angeles

printf "Updating\n"
sudo apt update -y &>> install.log
sudo apt upgrade -y &>> install.log
sudo apt dist-upgrade -y &>> install.log

printf "Command outputs are stored in install.log in this directory"

printf "Setting up .env file\n"
echo PYTHONPATH=${PYTHONPATH}:${PWD} >> .env
mkdir -p logs

./setup/install_py390.sh
./setup/i2c_setup.sh

# Install other dependencies
printf "Installing other dependencies"
sudo apt install cmake libssl-dev pipenv -y &>> install.log

pipenv install --dev

printf "To finish, restart: sudo restart"
printf "You will also need to copy the certificates folder\n"

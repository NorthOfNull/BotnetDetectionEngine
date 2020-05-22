#!/bin/bash
#
# Setup script to install necessary dependencies. 
#

# Get LFS Model files
sudo apt-get install git-lfs
sudo git lfs pull

# Python
sudo apt-get install python3-pip

pip3 install --upgrade pandas
pip3 install --upgrade scikit-learn==0.22.1
pip3 install --upgrade websocket-client
pip3 install --upgrade coverage


# Network Sniffer (argus and ra)
sudo apt-get install argus-server


# Node
rm -rf node_modules
mkdir node_modules

sudo apt-get install nodejs
sudo apt-get install npm

npm config set unsafe-perm true

npm install electron
npm install ws

sudo npm install -g


# Mark run file as executable
chmod u+x ./run.sh

#!/bin/bash
#
# Setup script to install necessary dependencies. 
#


# Python
sudo apt-get install python3-pip

sudo pip3 install --upgrade pandas
sudo pip3 install --upgrade scikit-learn==0.22.1
sudo pip3 install --upgrade websocket-client
sudo pip3 install --upgrade coverage


# Network Sniffer (argus and ra)
sudo apt-get install argus-server


# Node
sudo rm -rf node_modules
sudo mkdir node_modules

sudo apt-get install npm

sudo npm install -g electron --allow-root --unsafe-perm
sudo npm install -g ws --allow-root --unsafe-perm

sudo npm install -g --allow-root --unsafe-perm


# Mark run file as executable
sudo chmod +x ./run.sh

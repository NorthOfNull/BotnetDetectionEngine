# TODO:
# Setup script for detection software
# 
#	Python 3.7:
#		pip install websocket
#		pip install scikit-learn=0.22.1
#		pip install pandas
#
#	FOR SNIFFER:
#		tcpdump
#		argus
#			bison
#			flex
#			libcap? - might not need this if is installed via tcpdump install
#		ra client
#	
#	NODE JS ELECTRON STUFF? NPM?
# 


# Superuser


# Python
sudo apt-get install python3-pip

sudo pip3 install --upgrade pandas
sudo pip3 install --upgrade scikit-learn==0.22.1
sudo pip3 install --upgrade websocket-client
sudo pip3 install --upgrade coverage


# Network Sniffer
sudo apt-get install argus-server


# Node
sudo apt-get install npm

sudo npm install electron
sudo npm install ws


# Mark run file as executable
sudo chmod +x ./run.sh

#! /usr/bin/env bash

# -----------------------------------------------------------------
#   Installing additional dependency
#   Platform: Ubuntu 16.04 & HEC-HMS 4.2.1
#
#   binary-packages: (stated in release note)
#   	- gdal-bin (version > 2) 
#   	- libc6 	- libstdc++6 	- libncurses5
#   	- libxi6 	- libxrender1 	- libxtst6
#
#   python-packages: 
#   	- numpy		- scipy		- shapely 		- netcdf4 
#		- pandas 	- h5py		- tensorflow	- pyshp 
# -----------------------------------------------------------------

echo 'Installing required dependency...'

# add repository for gdal
sudo add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable

# enable i386 support
sudo dpkg --add-architecture i386
sudo apt update

sudo apt install -y libc6:i386 libstdc++6:i386 libncurses5:i386 \
					libxi6:i386 libgcc1:i386 libxrender1:i386 \
					libxtst6:i386 libstdc++6:i386 libc6-i386 \
					gdal-bin


sudo -H pip3 install -r requirements.txt --upgrade
#!/bin/bash

sudo apt-get update && sudo apt-get upgrade -y
sudo rpi-update -y

cd /media/pi/"$(ls /media/pi)/raspberry"
cp -r .config /home/pi/
cp -r Desktop /home/pi/
cp -r Documents /home/pi/
cp -r Banc_Robot /home/pi/
sudo cp ConfigFiles/config.txt /boot/config.txt
sudo cp ConfigFiles/pix.script /usr/share/plymouth/themes/pix/pix.script
sudo cp ConfigFiles/cron /etc/default/cron
sudo cp ConfigFiles/rsyslog.conf /etc/rsyslog.conf
sudo cp /media/pi/BANCBVR/Images/splashFARAL.png /usr/share/plymouth/themes/pix/splash.png
sudo cp /media/pi/BANCBVR/Images/backgroundFARAL.jpg /usr/share/rpd-wallpaper/temple.jpg

cd /home/pi/
sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev tar wget
wget https://www.python.org/ftp/python/3.9.1/Python-3.9.1.tgz
tar zxf Python-3.9.1.tgz
cd Python-3.9.1
sudo ./configure --enable-optimizations
sudo make -j 4
sudo make altinstall
cd ..
sudo rm Python-3.9.1.tar.xz --force
sudo rm -r Python-3.9.1 --force
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2 0
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1
sudo ln -s /usr/share/pyshared/lsb_release.py /usr/local/lib/python3.9/site-packages/lsb_release.py
sudo ln -s /usr/local/bin/python3.9 /usr/bin/python3.9
echo "alias python=/usr/local/bin/python3.9" >> ~/.bashrc
echo "alias python3=/usr/local/bin/python3.9" >> ~/.bashrc
source ~/.bashrc
cd ..
. ~/.bashrc
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.9 2
python -m pip install --upgrade pip

python -m pip install pandas
sudo apt-get install libjpeg-dev -y
sudo apt-get install zlib1g-dev -y
sudo apt-get install libfreetype6-dev -y
sudo apt-get install liblcms1-dev -y
sudo apt-get install libopenjp2-7 -y
sudo apt-get install libtiff5 -y
python -m pip install fpdf
python -m pip install pillow
python -m pip install Adafruit_MCP3008
python -m pip install matplotlib
python -m pip install RPi.GPIO

cd /media/pi/"$(ls /media/pi)/raspberry"
python ConfigFiles/edit.py
sudo cp ConfigFiles/cmdline.txt /boot/cmdline.txt

sudo apt-get remove dphys-swapfile -y

sudo apt-get autoremove -y
sudo apt-get autoclean -y

sudo reboot
#!/bin/bash

cd /media/pi/"$(ls /media/pi)/raspberry"
cp -r .config /home/pi/
cp -r Desktop /home/pi/
cp -r Documents /home/pi/
cp -r Banc_Robot /home/pi/
sudo cp ConfigFiles/config.txt /boot/config.txt
sudo cp ConfigFiles/cmdline.txt /boot/cmdline.txt
sudo cp ConfigFiles/pix.script /usr/share/plymouth/themes/pix/pix.script
sudo cp ConfigFiles/cron /etc/default/cron
sudo cp ConfigFiles/rsyslog.conf /etc/rsyslog.conf

alias python=python3
alias pip=pip3

pip install pandas
pip install pillow
pip install Adafruit_MCP3008
pip install matplotlib

sudo cp /media/pi/BANCBVR/Images/splashFARAL.png /usr/share/plymouth/themes/pix/splash.png
sudo cp /media/pi/BANCBVR/Images/backgroundFARAL.jpg /usr/share/rpd-wallpaper/temple.jpg

sudo apt-get remove dphys-swapfile

sudo reboot
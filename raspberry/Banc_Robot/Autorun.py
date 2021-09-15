import os
from time import sleep
import configparser
path = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read(path + '/Software/config.ini')
autoExe = bool(int(config['Launching_Options']['USBAutoExecution']))

while True:
	if not autoExe:
		break
	disks = os.popen("ls /media/pi").read()
	if disks != '':
		os.system("python " + path + "/Software/Main.py")
		break
	sleep(0.5)

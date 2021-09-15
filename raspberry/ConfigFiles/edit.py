import os
path = os.path.dirname(os.path.abspath(__file__))
sysboot = open("/boot/cmdline.txt")
content = sysboot.read()
partuuid = content[50:61]
usbboot = open(path + "/cmdline.txt")
content = usbboot.read()
content = content[:50] + partuuid + content[61:]
usbboot = open(path + "/cmdline.txt", 'w')
usbboot.write(content)
print('Changing the PARTUUID in cmdline.txt... Done')

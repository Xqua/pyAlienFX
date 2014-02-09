#!/usr/bin/python
# -*- coding: UTF-8 -*-

#This file is part of pyAlienFX.
#
#    pyAlienFX is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    pyAlienFX is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pyAlienFX.  If not, see <http://www.gnu.org/licenses/>.
#
#    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#    To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter
#    to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.
#

import os,sys
import platform
dist = platform.dist()[0]

if os.getuid() != 0:
	print "You must launch the installer script as root !"
	sys.exit(1)
BasePath = os.path.realpath('.')
thanksmsg = "Thanks !\nDevelopped by \033[1;30mXqua\033[0m"
print """
\033[1;32mWelcome to the \033[0m\033[1;31mpyAlienFX\033[0m\033[1;32m Installer script !\033[0m

You are about to configure the software : pyAlienFX !"""
if len(sys.argv) > 1:
	if sys.argv[1] != "deb":
		n = 0
		while True:
			q = raw_input("Do you want to continue \033[1;31m(Y/N)\033[0m ? ")
			if q.lower() == "n":
				print thanksmsg
				sys.exit(0)
			elif q.lower() == "y":
				break
			elif n == 3:
				print thanksmsg
				sys.exit(0)
			else:
				print "Please enter Y or N !"
			n += 1
	else:
		BasePath = "/usr/share/pyAlienFX"
		if not os.path.isdir(BasePath):
			os.mkdir(BasePath)

print """
\033[1;31m   !!! WARNING !!!\033[0m
The current version is packaged with a deamon running in the background as a TCP/IP server to control the lights.
First, this might/will cause trouble under windows systems
Second, this functionality is still in the Alpha stage and might cause unexpected bugs.
It is reccomended that you do not start the deamon automatically as you can still test it by launching the pyAlienFX_daemon.py script and then restarting the other pyAlienFX scripts."""
while True:
	q = raw_input('Do you wish to launch the deamon at startup ? \033[1;31m(Y/N)\033[0m ')

	if q.lower() == "y":
		optdeamon = ""
		break
	elif q.lower() == "n":
		optdeamon = "#"
		break
	elif q.lower() == "":
		optdeamon = "#"
		break
	else:
		print "Please answer Y or N (N)"
	

Bin = """#!/bin/sh
# -*- coding: UTF-8 -*-

#This file is part of pyAlienFX.
#
#    pyAlienFX is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    pyAlienFX is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pyAlienFX.  If not, see <http://www.gnu.org/licenses/>.
#
#    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#    To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter
#    to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.
#


#THIS FILE IS GENERATED WITH THE install.py file ! Do not modify it !


cd %s
gksudo ./pyAlienFX_Launcher.sh
"""%(BasePath)

Launcher = """#!/bin/sh
# -*- coding: UTF-8 -*-

#This file is part of pyAlienFX.
#
#    pyAlienFX is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    pyAlienFX is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pyAlienFX.  If not, see <http://www.gnu.org/licenses/>.
#
#    This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#    To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter
#    to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.
#

# This file will launch the deamon and the indicator applet !
# You should add it to your Session Auto Launch for a better experience !

#THIS FILE IS GENERATED WITH THE install.py file ! Do not modify it !


cd %s
%spython ./pyAlienFX_daemon.py &
%ssleep 5
python ./pyAlienFX_Indicator.py &
"""%(BasePath,optdeamon,optdeamon)

Unity = """[Desktop Entry]
Name=pyAlienFX
Comment=Launch the pyAlienFX Configurator
TryExec=pyAlienFX
Exec=pyAlienFX
Icon=%s/images/icon.png
Type=Application
Categories=Utility;
StartupNotify=true
OnlyShowIn=GNOME;Unity;
"""%(BasePath)
try:
	f = open('/usr/share/applications/pyAlienFX.desktop','w')
	f.write(Unity)
	f.close()
	if dist == "Ubuntu":
		f = open('/etc/xdg/autostart/pyAlienFX.desktop','w')
		f.write(Unity)
		f.close()
except:
	print "\033[1;31m !!! Please run the script as sudo in order to install the script in the Unity interface !!! \033[0m"
#os.setuid(1000)
#os.setgid(1001)

f = open('%s/pyAlienFX_Launcher.sh'%BasePath,'w')
f.write(Launcher)
f.close()
os.system('chmod 755 %s/pyAlienFX_Launcher.sh'%BasePath)

try:
	f = open('/usr/bin/pyAlienFX','w')
	f.write(Bin)
	f.close()
	os.system('chmod 755 /usr/bin/pyAlienFX')
except:
	f = open('%s/pyAlienFX'%BasePath,'w')
	f.write(Bin)
	f.close()
	os.system('chmod 755 %s/pyAlienFX'%BasePath)
	print "\033[1;31m !!! Please run the script as sudo in order to install the script correctly !!! \033[0m"

print "Thanks for installing !\n%s"%thanksmsg
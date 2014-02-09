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

import platform
import sys,os

class AlienFXProperties:
	def __init__(self):
		self.isDebug = False
		
		self.AUTHOR = "Blondel Leo"
		
		#Application info
		self.ALIEN_FX_VERSION = "pre alpha"
		self.ALIEN_FX_APPLICATION_RAW_NAME = "pyAlienFX"
		self.ALIEN_FX_APPLICATION_NAME = self.ALIEN_FX_APPLICATION_RAW_NAME +" "+ self.ALIEN_FX_VERSION
		
		#java properties
		self.PROPERTY_OS_NAME = platform.platform()
		self.USER_HOME = os.path.expanduser('~')
		self.JAVA_ARCHITECTURE = platform.machine()
		
		#used properties
		self.arch = platform.machine()
		self.userHomePath = os.path.expanduser('~')
		self.osName = sys.platform
		
		#OS checks
		self.WINDOWS_OS = "Windows"
		self.isWindows = self.isWindows()

		#native libraries
		self.ALIENFX_NATIVE_LIBRARY_NAME = "Alien"
		self.ALIENFX_NATIVE_LIBRARY = self.ALIENFX_NATIVE_LIBRARY_NAME+self.arch
		
		#powermodes and region ids
		self.ALIEN_FX_DEFAULT_POWER_MODE = ""
		self.POWER_BUTTON_ID = "PB"
		self.POWER_BUTTON_EYES_ID = "PBE"
		self.MEDIA_BAR_ID = "MB"
		self.TOUCH_PAD_ID = "TP"
		self.ALIEN_LOGO_ID = "AL"
		self.ALIEN_HEAD_ID = "AH"
		self.LEFT_SPEAKER_ID = "LS"
		self.RIGHT_SPEAKER_ID = "RS"
		self.LEFT_CENTER_KEYBOARD_ID = "LCK"
		self.LEFT_KEYBOARD_ID = "LK"
		self.RIGHT_CENTER_KEYBOARD_ID = "RCK"
		self.RIGHT_KEYBOARD_ID = "RK"
		self.LIGHT_PIPE_ID = "LP"
		self.KEYBOARD_ID = "KB"
		
		self.ON_BATTERY_ID = "BAT"
		self.CHARGING_ID = "CH"
		self.AC_POWER_ID = "AC"
		self.STANDBY_ID = "SB"
		
	def isWindows(self):
		if self.WINDOWS_OS in platform.platform():
			return True
		return False
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




from AlienFX.AlienFXProperties import *
from AlienFX.AlienFXTexts import *

	
class AlienFXPowerMode:
	def __init__(self, name, description, block):
		self.description = description
		#self.blockId = block
		self.name = name

class AlienFXRegion:
	def __init__(self, name, description, regionId, maxCommands, canBlink, canMorph, canLight, default_color, supportedModes, default_mode = "fixed", power_button = False):
		self.description = description
		self.regionId = regionId
		self.name = name
		self.canLight = canLight
		self.canBlink = canBlink
		self.canMorph = canMorph
		self.color1 = default_color
		self.color2 = default_color
		self.mode = default_mode
		self.power_button = power_button
		self.maxCommands = maxCommands
		self.supportedModes = supportedModes
		self.line = {1 : AlienFXConfiguration(self.mode,self.color1,self.color2)}
		
	def update_line(self,Id,mode=None,color1=None,color2=None):
		if self.line.has_key(Id):
			if mode:
				self.line[Id].mode = mode
			if color1:
				self.line[Id].color1 = color1
			if color2:
				self.line[Id].color2 = color2
			return True
		return False
	
	def add_line(self,Id,mode,color1,color2):
		Id = max(self.line.keys())
		if not self.line.has_key(Id+1):
			self.line[Id+1] = AlienFXConfiguration(mode,color1,color2)
			return True
		return False
	
class AlienFXConfiguration:
	def __init__(self,mode,color1,color2 = None):
		self.mode = mode
		self.color1 = color1
		self.color2 = color2
		
	def __str__(self):
		return "Mode : %s\nColor1 : %s\nColor2 : %s"%(self.mode,self.color1,self.color2)
		
class M11XR3:
	def __init__(self):
		self.AlienFXProperties = AlienFXProperties()
		self.AlienFXTexts = AlienFXTexts()
		self.regions = {}
		self.suportedMode = {}
		self.default_color = '0000FF'
		self.default_mode = "fixed"
		self.name = "M11XR3"
		#Define Alienware M11x Device Control
		self.STATE_BUSY = 0x11
		self.STATE_READY = 0x10
		self.STATE_UNKNOWN_COMMAND = 0x12
			
		self.SUPPORTED_COMMANDS = 15
		self.COMMAND_END_STORAGE = 0x00 # = End Storage block (See storage)
		self.COMMAND_SET_MORPH_COLOR = 0x01# = Set morph color (See set commands)
		self.COMMAND_SET_BLINK_COLOR = 0x02# = Set blink color (See set commands)
		self.COMMAND_SET_COLOR = 0x03# = Set color (See set commands)
		self.COMMAND_LOOP_BLOCK_END = 0x04# = Loop Block end (See loops)
		self.COMMAND_TRANSMIT_EXECUTE = 0x05# = End transmition and execute
		self.COMMAND_GET_STATUS = 0x06# = Get device status (see get device status)
		self.COMMAND_RESET = 0x07# = Reset (See reset)
		self.COMMAND_SAVE_NEXT = 0x08# = Save next instruction in storage block (see storage)
		self.COMMAND_SAVE = 0x09# = Save storage data (See storage)
		self.COMMAND_BATTERY_STATE = 0x0F# = Set batery state (See set commands)
		self.COMMAND_SET_SPEED = 0x0E# = Set display speed (see set speed)
			
		self.RESET_TOUCH_CONTROLS = 0x01
		self.RESET_SLEEP_LIGHTS_ON = 0x02
		self.RESET_ALL_LIGHTS_OFF = 0x03
		self.RESET_ALL_LIGHTS_ON = 0x04
			
		self.DATA_LENGTH = 9
			
		self.START_BYTE = 0x02
		self.FILL_BYTE = 0x00
			
		self.BLOCK_LOAD_ON_BOOT = 0x01
		self.BLOCK_STANDBY = 0x02
		self.BLOCK_AC_POWER = 0x05
		self.BLOCK_CHARGING = 0x06
		self.BLOCK_BATT_SLEEPING = 0x07
		self.BLOCK_BAT_POWER = 0x08
		self.BLOCK_BATT_CRITICAL = 0x09
			
		self.REGION_RIGHT_KEYBOARD = 0x0001 
		self.REGION_RIGHT_SPEAKER = 0x0020 
		self.REGION_LEFT_SPEAKER = 0x0040
		self.REGION_ALIEN_NAME = 0x0100 
		self.REGION_MEDIA_BAR = 0x0800
		self.REGION_POWER_BUTTON = 0x6000
		self.REGION_ALL_BUT_POWER = 0x0f9fff 
		
		self.suportedMode["normal"] = AlienFXPowerMode(self.AlienFXProperties.ALIEN_FX_DEFAULT_POWER_MODE,self.AlienFXProperties.ALIEN_FX_DEFAULT_POWER_MODE, self.BLOCK_LOAD_ON_BOOT),
		self.suportedMode["standby"] = AlienFXPowerMode(self.AlienFXProperties.STANDBY_ID, self.AlienFXTexts.STAND_BY_DESCRIPTION, self.BLOCK_STANDBY),
		self.suportedMode["acPower"] = AlienFXPowerMode(self.AlienFXProperties.AC_POWER_ID, self.AlienFXTexts.AC_POWER_DESCRIPTION, self.BLOCK_AC_POWER),
		self.suportedMode["charging"] = AlienFXPowerMode(self.AlienFXProperties.CHARGING_ID, self.AlienFXTexts.CHARGING2_DESCRIPTION, self.BLOCK_CHARGING),
		self.suportedMode["onBat"] = AlienFXPowerMode(self.AlienFXProperties.ON_BATTERY_ID, self.AlienFXTexts.ON_BATTERY_DESCRIPTION, self.BLOCK_BAT_POWER)
		
		self.regions[self.AlienFXProperties.RIGHT_KEYBOARD_ID] = AlienFXRegion(self.AlienFXProperties.RIGHT_KEYBOARD_ID, self.AlienFXTexts.KEYBOARD_DESCRIPTION, self.REGION_RIGHT_KEYBOARD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.RIGHT_SPEAKER_ID] = AlienFXRegion(self.AlienFXProperties.RIGHT_SPEAKER_ID, self.AlienFXTexts.RIGHT_SPEAKER_DESCRIPTION, self.REGION_RIGHT_SPEAKER,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.LEFT_SPEAKER_ID] = AlienFXRegion(self.AlienFXProperties.LEFT_SPEAKER_ID, self.AlienFXTexts.LEFT_SPEAKER_DESCRIPTION, self.REGION_LEFT_SPEAKER,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.ALIEN_LOGO_ID] = AlienFXRegion(self.AlienFXProperties.ALIEN_LOGO_ID, self.AlienFXTexts.ALIENWARE_LOGO_DESCRIPTION, self.REGION_ALIEN_NAME,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.MEDIA_BAR_ID] = AlienFXRegion(self.AlienFXProperties.MEDIA_BAR_ID, self.AlienFXTexts.MEDIA_BAR_DESCRIPTION, self.REGION_MEDIA_BAR,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.POWER_BUTTON_ID] = AlienFXRegion(self.AlienFXProperties.POWER_BUTTON_ID, self.AlienFXTexts.POWER_BUTTON_DESCRIPTION, self.REGION_POWER_BUTTON,2,False,True,False, self.default_color , self.suportedMode, power_button = True)

#added by LightHash [start]
class M14XLight:
	def __init__(self):

		self.AlienFXProperties = AlienFXProperties()
		self.AlienFXTexts = AlienFXTexts()
		self.regions = {}
		self.suportedMode = {}
		self.default_color = '0000FF'
		self.default_mode = "fixed"
		self.name = "M14XR1"

		self.STATE_BUSY = 0x11
		self.STATE_READY = 0x10
		self.STATE_UNKNOWN_COMMAND = 0x12

		self.SUPPORTED_COMMANDS = 15
		self.COMMAND_END_STORAGE = 0x00# = End Storage block (See storage)
		self.COMMAND_SET_MORPH_COLOR = 0x01# = Set morph color (See set commands)
		self.COMMAND_SET_BLINK_COLOR = 0x02# = Set blink color (See set commands)
		self.COMMAND_SET_COLOR = 0x03# = Set color (See set commands)
		self.COMMAND_LOOP_BLOCK_END = 0x04# = Loop Block end (See loops)
		self.COMMAND_TRANSMIT_EXECUTE = 0x05# = End transmition and execute
		self.COMMAND_GET_STATUS = 0x06# = Get device status (see get device status)
		self.COMMAND_RESET = 0x07# = Reset (See reset)
		self.COMMAND_SAVE_NEXT = 0x08# = Save next instruction in storage block (see storage)
		self.COMMAND_SAVE = 0x09# = Save storage data (See storage)
		self.COMMAND_BATTERY_STATE = 0x0F# = Set batery state (See set commands)
		self.COMMAND_SET_SPEED = 0x0E# = Set display speed (see set speed)

		self.RESET_TOUCH_CONTROLS = 0x01
		self.RESET_SLEEP_LIGHTS_ON = 0x02
		self.RESET_ALL_LIGHTS_OFF = 0x03
		self.RESET_ALL_LIGHTS_ON = 0x04

		self.DATA_LENGTH = 9

		self.START_BYTE = 0x02
		self.FILL_BYTE = 0x00

		self.BLOCK_LOAD_ON_BOOT = 0x01
		self.BLOCK_STANDBY = 0x02
		self.BLOCK_AC_POWER = 0x05
		self.BLOCK_CHARGING = 0x06

		self.BLOCK_BATT_CRITICAL = 0x07
		self.BLOCK_BAT_POWER = 0x08

		self.REGION_RIGHT_KEYBOARD = 0x0001
		self.REGION_MIDDLE_RIGHT_KEYBOARD = 0x0002
		self.REGION_LEFT_KEYBOARD = 0x0008
		self.REGION_MIDDLE_LEFT_KEYBOARD = 0x0004
		self.REGION_POWER_BUTTON_2 = 0x0010
		self.REGION_RIGHT_SPEAKER = 0x0020
		self.REGION_LEFT_SPEAKER = 0x0040
		self.REGION_ALIEN_HEAD = 0x0080
		self.REGION_ALIEN_NAME = 0x0100
		self.REGION_TOUCH_PAD = 0x0200
		self.REGION_MEDIA_BAR = 0x1c00
		self.REGION_POWER_BUTTON = 0x2000
		self.REGION_POWER_BUTTON_EYES = 0x4000
		self.REGION_ALL_BUT_POWER = 0x0f9fff

		self.suportedMode["normal"] = AlienFXPowerMode(self.AlienFXProperties.ALIEN_FX_DEFAULT_POWER_MODE,self.AlienFXProperties.ALIEN_FX_DEFAULT_POWER_MODE, self.BLOCK_LOAD_ON_BOOT)
		self.suportedMode["standby"] = AlienFXPowerMode(self.AlienFXProperties.STANDBY_ID, self.AlienFXTexts.STAND_BY_DESCRIPTION, self.BLOCK_STANDBY)
		self.suportedMode["acPower"] = AlienFXPowerMode(self.AlienFXProperties.AC_POWER_ID, self.AlienFXTexts.AC_POWER_DESCRIPTION, self.BLOCK_AC_POWER)
		self.suportedMode["charging"] = AlienFXPowerMode(self.AlienFXProperties.CHARGING_ID, self.AlienFXTexts.CHARGING2_DESCRIPTION, self.BLOCK_CHARGING)
		self.suportedMode["onBat"] = AlienFXPowerMode(self.AlienFXProperties.ON_BATTERY_ID, self.AlienFXTexts.ON_BATTERY_DESCRIPTION, self.BLOCK_BAT_POWER)


		self.regions[self.AlienFXProperties.RIGHT_KEYBOARD_ID] = AlienFXRegion(self.AlienFXProperties.RIGHT_KEYBOARD_ID,  self.AlienFXTexts.RIGHT_KEYBOARD_DESCRIPTION, self.REGION_RIGHT_KEYBOARD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.RIGHT_CENTER_KEYBOARD_ID] = AlienFXRegion(self.AlienFXProperties.RIGHT_CENTER_KEYBOARD_ID, self.AlienFXTexts.RIGHT_CENTER_KEYBOARD_DESCRIPTION, self.REGION_MIDDLE_RIGHT_KEYBOARD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.LEFT_KEYBOARD_ID] = AlienFXRegion(self.AlienFXProperties.LEFT_KEYBOARD_ID,  self.AlienFXTexts.LEFT_KEYBOARD_DESCRIPTION, self.REGION_LEFT_KEYBOARD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.LEFT_CENTER_KEYBOARD_ID] = AlienFXRegion(self.AlienFXProperties.LEFT_CENTER_KEYBOARD_ID, self.AlienFXTexts.LEFT_CENTER_KEYBOARD_DESCRIPTION, self.REGION_MIDDLE_LEFT_KEYBOARD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.RIGHT_SPEAKER_ID] = AlienFXRegion(self.AlienFXProperties.RIGHT_SPEAKER_ID,  self.AlienFXTexts.RIGHT_SPEAKER_DESCRIPTION, self.REGION_RIGHT_SPEAKER,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.LEFT_SPEAKER_ID] = AlienFXRegion(self.AlienFXProperties.LEFT_SPEAKER_ID,  self.AlienFXTexts.LEFT_SPEAKER_DESCRIPTION, self.REGION_LEFT_SPEAKER,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.ALIEN_HEAD_ID] = AlienFXRegion(self.AlienFXProperties.ALIEN_HEAD_ID,  self.AlienFXTexts.ALIENWARE_HEAD_DESCRIPTION, self.REGION_ALIEN_HEAD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.ALIEN_LOGO_ID] = AlienFXRegion(self.AlienFXProperties.ALIEN_LOGO_ID,  self.AlienFXTexts.ALIENWARE_LOGO_DESCRIPTION, self.REGION_ALIEN_NAME,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.TOUCH_PAD_ID] = AlienFXRegion(self.AlienFXProperties.TOUCH_PAD_ID,  self.AlienFXTexts.TOUCHPAD_DESCRIPTION, self.REGION_TOUCH_PAD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.MEDIA_BAR_ID] = AlienFXRegion(self.AlienFXProperties.MEDIA_BAR_ID,  self.AlienFXTexts.MEDIA_BAR_DESCRIPTION, self.REGION_MEDIA_BAR,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.POWER_BUTTON_EYES_ID] = AlienFXRegion(self.AlienFXProperties.POWER_BUTTON_EYES_ID, self.AlienFXTexts.ALIENWARE_POWERBUTTON_EYES_DESCRIPTION, self.REGION_POWER_BUTTON_EYES,1,False,False,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.POWER_BUTTON_ID] = AlienFXRegion(self.AlienFXProperties.POWER_BUTTON_ID, self.AlienFXTexts.POWER_BUTTON_DESCRIPTION, self.REGION_POWER_BUTTON,2,True,True,True, self.default_color , self.suportedMode, power_button = True)
#added by LightHash [end]

		
class M15XArea51:
	def __init__(self):
		self.AlienFXProperties = AlienFXProperties()
		self.AlienFXTexts = AlienFXTexts()
		self.regions = {}
		self.suportedMode = {}
		self.default_color = '0000FF'
		self.default_mode = "fixed"
		self.name = "M15XArea51"
		self.SUPPORTED_COMMANDS = 15
		self.STATE_BUSY = 0x11
		self.STATE_READY = 0x10
		self.STATE_UNKNOWN_COMMAND = 0x12
		
		self.COMMAND_END_STORAGE = 0x00# = End Storage block (See storage)
		self.COMMAND_SET_MORPH_COLOR = 0x01# = Set morph color (See set commands)
		self.COMMAND_SET_BLINK_COLOR = 0x02# = Set blink color (See set commands)
		self.COMMAND_SET_COLOR = 0x03# = Set color (See set commands)
		self.COMMAND_LOOP_BLOCK_END = 0x04# = Loop Block end (See loops)
		self.COMMAND_TRANSMIT_EXECUTE = 0x05# = End transmition and execute
		self.COMMAND_GET_STATUS = 0x06# = Get device status (see get device status)
		self.COMMAND_RESET = 0x07# = Reset (See reset)
		self.COMMAND_SAVE_NEXT = 0x08# = Save next instruction in storage block (see storage)
		self.COMMAND_SAVE = 0x09# = Save storage data (See storage)
		self.COMMAND_BATTERY_STATE = 0x0F# = Set batery state (See set commands)
		self.COMMAND_SET_SPEED = 0x0E# = Set display speed (see set speed)
		
		self.RESET_TOUCH_CONTROLS = 0x01
		self.RESET_SLEEP_LIGHTS_ON = 0x02
		self.RESET_ALL_LIGHTS_OFF = 0x03
		self.RESET_ALL_LIGHTS_ON = 0x04
		
		self.DATA_LENGTH = 9
		
		self.START_BYTE = 0x00
		self.FILL_BYTE = 0x00
		
		self.BLOCK_LOAD_ON_BOOT = 0x01
		self.BLOCK_STANDBY = 0x02
		self.BLOCK_AC_POWER = 0x05
		self.BLOCK_CHARGING = 0x06
		self.BLOCK_BAT_POWER = 0x08
		
		self.REGION_TOUCH_PAD = 0x000001
		self.REGION_LIGHTPIPE = 0x000020 
		self.REGION_ALIEN_LOGO = 0x000080 
		self.REGION_ALIEN_HEAD = 0x000100
		self.REGION_KEY_BOARD = 0x000400
		self.REGION_TOUCH_PANEL = 0x010000 
		self.REGION_POWER_BUTTON = 0x008000
		self.REGION_ALL_BUT_POWER = 0x0f9fff
		
		self.suportedMode["normal"] = AlienFXPowerMode(self.AlienFXProperties.ALIEN_FX_DEFAULT_POWER_MODE,self.AlienFXProperties.ALIEN_FX_DEFAULT_POWER_MODE, self.BLOCK_LOAD_ON_BOOT)
		self.suportedMode["standby"] = AlienFXPowerMode(self.AlienFXProperties.STANDBY_ID, self.AlienFXTexts.STAND_BY_DESCRIPTION, self.BLOCK_STANDBY)
		self.suportedMode["acPower"] = AlienFXPowerMode(self.AlienFXProperties.AC_POWER_ID, self.AlienFXTexts.AC_POWER_DESCRIPTION, self.BLOCK_AC_POWER)
		self.suportedMode["charging"] = AlienFXPowerMode(self.AlienFXProperties.CHARGING_ID, self.AlienFXTexts.CHARGING2_DESCRIPTION, self.BLOCK_CHARGING)
		self.suportedMode["onBat"] = AlienFXPowerMode(self.AlienFXProperties.ON_BATTERY_ID, self.AlienFXTexts.ON_BATTERY_DESCRIPTION, self.BLOCK_BAT_POWER)

		self.regions[self.AlienFXProperties.LIGHT_PIPE_ID] = AlienFXRegion(self.AlienFXProperties.LIGHT_PIPE_ID, self.AlienFXTexts.LIGHT_PIPE_DESCRIPTION, self.REGION_LIGHTPIPE,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.KEYBOARD_ID] = AlienFXRegion(self.AlienFXProperties.KEYBOARD_ID, self.AlienFXTexts.KEYBOARD_DESCRIPTION, self.REGION_KEY_BOARD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.ALIEN_HEAD_ID] = AlienFXRegion(self.AlienFXProperties.ALIEN_HEAD_ID, self.AlienFXTexts.ALIENWARE_HEAD_DESCRIPTION, self.REGION_ALIEN_HEAD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.ALIEN_LOGO_ID] = AlienFXRegion(self.AlienFXProperties.ALIEN_LOGO_ID, self.AlienFXTexts.ALIENWARE_LOGO_DESCRIPTION, self.REGION_ALIEN_LOGO,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.TOUCH_PAD_ID] = AlienFXRegion(self.AlienFXProperties.TOUCH_PAD_ID, self.AlienFXTexts.TOUCHPAD_DESCRIPTION, self.REGION_TOUCH_PAD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.MEDIA_BAR_ID] = AlienFXRegion(self.AlienFXProperties.MEDIA_BAR_ID, self.AlienFXTexts.MEDIA_BAR_DESCRIPTION, self.REGION_TOUCH_PANEL,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.POWER_BUTTON_ID] = AlienFXRegion(self.AlienFXProperties.POWER_BUTTON_ID, self.AlienFXTexts.POWER_BUTTON_DESCRIPTION, self.REGION_POWER_BUTTON,1,False,False,True, self.default_color , self.suportedMode, power_button = True)
		
		
		

class M15XAllPowerfull:
	def __init__(self):
		
		self.AlienFXProperties = AlienFXProperties()
		self.AlienFXTexts = AlienFXTexts()
		self.regions = {}
		self.suportedMode = {}
		self.default_color = '0000FF'
		self.default_mode = "fixed"
		self.name = "M15XAllPowerful"
		
		self.STATE_BUSY = 0x11
		self.STATE_READY = 0x10
		self.STATE_UNKNOWN_COMMAND = 0x12
		
		self.SUPPORTED_COMMANDS = 15
		self.COMMAND_END_STORAGE = 0x00# = End Storage block (See storage)
		self.COMMAND_SET_MORPH_COLOR = 0x01# = Set morph color (See set commands)
		self.COMMAND_SET_BLINK_COLOR = 0x02# = Set blink color (See set commands)
		self.COMMAND_SET_COLOR = 0x03# = Set color (See set commands)
		self.COMMAND_LOOP_BLOCK_END = 0x04# = Loop Block end (See loops)
		self.COMMAND_TRANSMIT_EXECUTE = 0x05# = End transmition and execute
		self.COMMAND_GET_STATUS = 0x06# = Get device status (see get device status)
		self.COMMAND_RESET = 0x07# = Reset (See reset)
		self.COMMAND_SAVE_NEXT = 0x08# = Save next instruction in storage block (see storage)
		self.COMMAND_SAVE = 0x09# = Save storage data (See storage)
		self.COMMAND_BATTERY_STATE = 0x0F# = Set batery state (See set commands)
		self.COMMAND_SET_SPEED = 0x0E# = Set display speed (see set speed)
		
		self.RESET_TOUCH_CONTROLS = 0x01
		self.RESET_SLEEP_LIGHTS_ON = 0x02
		self.RESET_ALL_LIGHTS_OFF = 0x03
		self.RESET_ALL_LIGHTS_ON = 0x04
		
		self.DATA_LENGTH = 9
		
		self.START_BYTE = 0x02
		self.FILL_BYTE = 0x00
		
		self.BLOCK_LOAD_ON_BOOT = 0x01
		self.BLOCK_STANDBY = 0x02
		self.BLOCK_AC_POWER = 0x05
		self.BLOCK_CHARGING = 0x06
		
		self.BLOCK_BATT_CRITICAL = 0x07
		self.BLOCK_BAT_POWER = 0x08
		
		self.REGION_RIGHT_KEYBOARD = 0x0001 
		self.REGION_MIDDLE_RIGHT_KEYBOARD = 0x0002 
		self.REGION_LEFT_KEYBOARD = 0x0004 
		self.REGION_MIDDLE_LEFT_KEYBOARD = 0x0008 
		self.REGION_POWER_BUTTON_2 = 0x0010 
		self.REGION_RIGHT_SPEAKER = 0x0020 
		self.REGION_LEFT_SPEAKER = 0x0040
		self.REGION_ALIEN_HEAD = 0x0080 
		self.REGION_ALIEN_NAME = 0x0100 
		self.REGION_TOUCH_PAD = 0x0200 
		self.REGION_MEDIA_BAR = 0x1c00
		self.REGION_POWER_BUTTON = 0x2000 
		self.REGION_POWER_BUTTON_EYES = 0x4000
		self.REGION_ALL_BUT_POWER = 0x0f9fff
		
		self.suportedMode["normal"] = AlienFXPowerMode(self.AlienFXProperties.ALIEN_FX_DEFAULT_POWER_MODE,self.AlienFXProperties.ALIEN_FX_DEFAULT_POWER_MODE, self.BLOCK_LOAD_ON_BOOT)
		self.suportedMode["standby"] = AlienFXPowerMode(self.AlienFXProperties.STANDBY_ID, self.AlienFXTexts.STAND_BY_DESCRIPTION, self.BLOCK_STANDBY)
		self.suportedMode["acPower"] = AlienFXPowerMode(self.AlienFXProperties.AC_POWER_ID, self.AlienFXTexts.AC_POWER_DESCRIPTION, self.BLOCK_AC_POWER)
		self.suportedMode["charging"] = AlienFXPowerMode(self.AlienFXProperties.CHARGING_ID, self.AlienFXTexts.CHARGING2_DESCRIPTION, self.BLOCK_CHARGING)
		self.suportedMode["onBat"] = AlienFXPowerMode(self.AlienFXProperties.ON_BATTERY_ID, self.AlienFXTexts.ON_BATTERY_DESCRIPTION, self.BLOCK_BAT_POWER)
		
		
		self.regions[self.AlienFXProperties.RIGHT_KEYBOARD_ID] = AlienFXRegion(self.AlienFXProperties.RIGHT_KEYBOARD_ID,  self.AlienFXTexts.RIGHT_KEYBOARD_DESCRIPTION, self.REGION_RIGHT_KEYBOARD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.RIGHT_CENTER_KEYBOARD_ID] = AlienFXRegion(self.AlienFXProperties.RIGHT_CENTER_KEYBOARD_ID, self.AlienFXTexts.RIGHT_CENTER_KEYBOARD_DESCRIPTION, self.REGION_MIDDLE_RIGHT_KEYBOARD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.LEFT_KEYBOARD_ID] = AlienFXRegion(self.AlienFXProperties.LEFT_KEYBOARD_ID,  self.AlienFXTexts.LEFT_KEYBOARD_DESCRIPTION, self.REGION_LEFT_KEYBOARD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.LEFT_CENTER_KEYBOARD_ID] = AlienFXRegion(self.AlienFXProperties.LEFT_CENTER_KEYBOARD_ID, self.AlienFXTexts.LEFT_CENTER_KEYBOARD_DESCRIPTION, self.REGION_MIDDLE_LEFT_KEYBOARD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.RIGHT_SPEAKER_ID] = AlienFXRegion(self.AlienFXProperties.RIGHT_SPEAKER_ID,  self.AlienFXTexts.RIGHT_SPEAKER_DESCRIPTION, self.REGION_RIGHT_SPEAKER,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.LEFT_SPEAKER_ID] = AlienFXRegion(self.AlienFXProperties.LEFT_SPEAKER_ID,  self.AlienFXTexts.LEFT_SPEAKER_DESCRIPTION, self.REGION_LEFT_SPEAKER,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.ALIEN_HEAD_ID] = AlienFXRegion(self.AlienFXProperties.ALIEN_HEAD_ID,  self.AlienFXTexts.ALIENWARE_HEAD_DESCRIPTION, self.REGION_ALIEN_HEAD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.ALIEN_LOGO_ID] = AlienFXRegion(self.AlienFXProperties.ALIEN_LOGO_ID,  self.AlienFXTexts.ALIENWARE_LOGO_DESCRIPTION, self.REGION_ALIEN_NAME,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.TOUCH_PAD_ID] = AlienFXRegion(self.AlienFXProperties.TOUCH_PAD_ID,  self.AlienFXTexts.TOUCHPAD_DESCRIPTION, self.REGION_TOUCH_PAD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.MEDIA_BAR_ID] = AlienFXRegion(self.AlienFXProperties.MEDIA_BAR_ID,  self.AlienFXTexts.MEDIA_BAR_DESCRIPTION, self.REGION_MEDIA_BAR,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.POWER_BUTTON_EYES_ID] = AlienFXRegion(self.AlienFXProperties.POWER_BUTTON_EYES_ID, self.AlienFXTexts.ALIENWARE_POWERBUTTON_EYES_DESCRIPTION, self.REGION_POWER_BUTTON_EYES,1,False,False,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.POWER_BUTTON_ID] = AlienFXRegion(self.AlienFXProperties.POWER_BUTTON_ID, self.AlienFXTexts.POWER_BUTTON_DESCRIPTION, self.REGION_POWER_BUTTON,2,True,True,True, self.default_color , self.suportedMode, power_button = True)

#############################################################
#added by niai (start)
class M17XR3:
	def __init__(self):
		
		self.AlienFXProperties = AlienFXProperties()
		self.AlienFXTexts = AlienFXTexts()
		self.regions = {}
		self.suportedMode = {}
		self.default_color = '0000FF'
		self.default_mode = "fixed"
		self.name = "M17XR3"
		
		self.STATE_BUSY = 0x11
		self.STATE_READY = 0x10
		self.STATE_UNKNOWN_COMMAND = 0x12
		
		self.SUPPORTED_COMMANDS = 15
		self.COMMAND_END_STORAGE = 0x00# = End Storage block (See storage)
		self.COMMAND_SET_MORPH_COLOR = 0x01# = Set morph color (See set commands)
		self.COMMAND_SET_BLINK_COLOR = 0x02# = Set blink color (See set commands)
		self.COMMAND_SET_COLOR = 0x03# = Set color (See set commands)
		self.COMMAND_LOOP_BLOCK_END = 0x04# = Loop Block end (See loops)
		self.COMMAND_TRANSMIT_EXECUTE = 0x05# = End transmition and execute
		self.COMMAND_GET_STATUS = 0x06# = Get device status (see get device status)
		self.COMMAND_RESET = 0x07# = Reset (See reset)
		self.COMMAND_SAVE_NEXT = 0x08# = Save next instruction in storage block (see storage)
		self.COMMAND_SAVE = 0x09# = Save storage data (See storage)
		self.COMMAND_BATTERY_STATE = 0x0F# = Set batery state (See set commands)
		self.COMMAND_SET_SPEED = 0x0E# = Set display speed (see set speed)
		
		self.RESET_TOUCH_CONTROLS = 0x01
		self.RESET_SLEEP_LIGHTS_ON = 0x02
		self.RESET_ALL_LIGHTS_OFF = 0x03
		self.RESET_ALL_LIGHTS_ON = 0x04
		
		self.DATA_LENGTH = 9
		
		self.START_BYTE = 0x02
		self.FILL_BYTE = 0x00
		
		self.BLOCK_LOAD_ON_BOOT = 0x01
		self.BLOCK_STANDBY = 0x02
		self.BLOCK_AC_POWER = 0x05
		self.BLOCK_CHARGING = 0x06
		
		self.BLOCK_BATT_CRITICAL = 0x07
		self.BLOCK_BAT_POWER = 0x08
		
		self.REGION_RIGHT_KEYBOARD = 0x0001 
		self.REGION_MIDDLE_RIGHT_KEYBOARD = 0x0002 
		self.REGION_LEFT_KEYBOARD = 0x0008 
		self.REGION_MIDDLE_LEFT_KEYBOARD = 0x0004 
		self.REGION_POWER_BUTTON_2 = 0x0010 
		self.REGION_RIGHT_SPEAKER = 0x0020 
		self.REGION_LEFT_SPEAKER = 0x0040
		self.REGION_ALIEN_HEAD = 0x0080 
		self.REGION_ALIEN_NAME = 0x0100 
		self.REGION_TOUCH_PAD = 0x0200 
		self.REGION_MEDIA_BAR = 0x1c00
		self.REGION_POWER_BUTTON = 0x2000 
		self.REGION_POWER_BUTTON_EYES = 0x4000
		self.REGION_ALL_BUT_POWER = 0x0f9fff
		
		self.suportedMode["normal"] = AlienFXPowerMode(self.AlienFXProperties.ALIEN_FX_DEFAULT_POWER_MODE,self.AlienFXProperties.ALIEN_FX_DEFAULT_POWER_MODE, self.BLOCK_LOAD_ON_BOOT)
		self.suportedMode["standby"] = AlienFXPowerMode(self.AlienFXProperties.STANDBY_ID, self.AlienFXTexts.STAND_BY_DESCRIPTION, self.BLOCK_STANDBY)
		self.suportedMode["acPower"] = AlienFXPowerMode(self.AlienFXProperties.AC_POWER_ID, self.AlienFXTexts.AC_POWER_DESCRIPTION, self.BLOCK_AC_POWER)
		self.suportedMode["charging"] = AlienFXPowerMode(self.AlienFXProperties.CHARGING_ID, self.AlienFXTexts.CHARGING2_DESCRIPTION, self.BLOCK_CHARGING)
		self.suportedMode["onBat"] = AlienFXPowerMode(self.AlienFXProperties.ON_BATTERY_ID, self.AlienFXTexts.ON_BATTERY_DESCRIPTION, self.BLOCK_BAT_POWER)
		
		
		self.regions[self.AlienFXProperties.RIGHT_KEYBOARD_ID] = AlienFXRegion(self.AlienFXProperties.RIGHT_KEYBOARD_ID,  self.AlienFXTexts.RIGHT_KEYBOARD_DESCRIPTION, self.REGION_RIGHT_KEYBOARD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.RIGHT_CENTER_KEYBOARD_ID] = AlienFXRegion(self.AlienFXProperties.RIGHT_CENTER_KEYBOARD_ID, self.AlienFXTexts.RIGHT_CENTER_KEYBOARD_DESCRIPTION, self.REGION_MIDDLE_RIGHT_KEYBOARD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.LEFT_KEYBOARD_ID] = AlienFXRegion(self.AlienFXProperties.LEFT_KEYBOARD_ID,  self.AlienFXTexts.LEFT_KEYBOARD_DESCRIPTION, self.REGION_LEFT_KEYBOARD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.LEFT_CENTER_KEYBOARD_ID] = AlienFXRegion(self.AlienFXProperties.LEFT_CENTER_KEYBOARD_ID, self.AlienFXTexts.LEFT_CENTER_KEYBOARD_DESCRIPTION, self.REGION_MIDDLE_LEFT_KEYBOARD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.RIGHT_SPEAKER_ID] = AlienFXRegion(self.AlienFXProperties.RIGHT_SPEAKER_ID,  self.AlienFXTexts.RIGHT_SPEAKER_DESCRIPTION, self.REGION_RIGHT_SPEAKER,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.LEFT_SPEAKER_ID] = AlienFXRegion(self.AlienFXProperties.LEFT_SPEAKER_ID,  self.AlienFXTexts.LEFT_SPEAKER_DESCRIPTION, self.REGION_LEFT_SPEAKER,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.ALIEN_HEAD_ID] = AlienFXRegion(self.AlienFXProperties.ALIEN_HEAD_ID,  self.AlienFXTexts.ALIENWARE_HEAD_DESCRIPTION, self.REGION_ALIEN_HEAD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.ALIEN_LOGO_ID] = AlienFXRegion(self.AlienFXProperties.ALIEN_LOGO_ID,  self.AlienFXTexts.ALIENWARE_LOGO_DESCRIPTION, self.REGION_ALIEN_NAME,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.TOUCH_PAD_ID] = AlienFXRegion(self.AlienFXProperties.TOUCH_PAD_ID,  self.AlienFXTexts.TOUCHPAD_DESCRIPTION, self.REGION_TOUCH_PAD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.MEDIA_BAR_ID] = AlienFXRegion(self.AlienFXProperties.MEDIA_BAR_ID,  self.AlienFXTexts.MEDIA_BAR_DESCRIPTION, self.REGION_MEDIA_BAR,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.POWER_BUTTON_EYES_ID] = AlienFXRegion(self.AlienFXProperties.POWER_BUTTON_EYES_ID, self.AlienFXTexts.ALIENWARE_POWERBUTTON_EYES_DESCRIPTION, self.REGION_POWER_BUTTON_EYES,1,False,False,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.POWER_BUTTON_ID] = AlienFXRegion(self.AlienFXProperties.POWER_BUTTON_ID, self.AlienFXTexts.POWER_BUTTON_DESCRIPTION, self.REGION_POWER_BUTTON,2,True,True,True, self.default_color , self.suportedMode, power_button = True)
#added by niai (end)
##############################################################################################

#############################################################
#added by SuperTool (start)
class M18XR2:
	def __init__(self):

		self.AlienFXProperties = AlienFXProperties()
		self.AlienFXTexts = AlienFXTexts()
		self.regions = {}
		self.suportedMode = {}
		self.default_color = '0000FF'
		self.default_mode = "fixed"
		self.name = "M18XR2"

		self.STATE_BUSY = 0x11
		self.STATE_READY = 0x10
		self.STATE_UNKNOWN_COMMAND = 0x12

		self.SUPPORTED_COMMANDS = 15
		self.COMMAND_END_STORAGE = 0x00# = End Storage block (See storage)
		self.COMMAND_SET_MORPH_COLOR = 0x01# = Set morph color (See set commands)
		self.COMMAND_SET_BLINK_COLOR = 0x02# = Set blink color (See set commands)
		self.COMMAND_SET_COLOR = 0x03# = Set color (See set commands)
		self.COMMAND_LOOP_BLOCK_END = 0x04# = Loop Block end (See loops)
		self.COMMAND_TRANSMIT_EXECUTE = 0x05# = End transmition and execute
		self.COMMAND_GET_STATUS = 0x06# = Get device status (see get device status)
		self.COMMAND_RESET = 0x07# = Reset (See reset)
		self.COMMAND_SAVE_NEXT = 0x08# = Save next instruction in storage block (see storage)
		self.COMMAND_SAVE = 0x09# = Save storage data (See storage)
		self.COMMAND_BATTERY_STATE = 0x0F# = Set batery state (See set commands)
		self.COMMAND_SET_SPEED = 0x0E# = Set display speed (see set speed)

		self.RESET_TOUCH_CONTROLS = 0x01
		self.RESET_SLEEP_LIGHTS_ON = 0x02
		self.RESET_ALL_LIGHTS_OFF = 0x03
		self.RESET_ALL_LIGHTS_ON = 0x04

		self.DATA_LENGTH = 9

		self.START_BYTE = 0x02
		self.FILL_BYTE = 0x00

		self.BLOCK_LOAD_ON_BOOT = 0x01
		self.BLOCK_STANDBY = 0x02
		self.BLOCK_AC_POWER = 0x05
		self.BLOCK_CHARGING = 0x06

		self.BLOCK_BATT_CRITICAL = 0x07
		self.BLOCK_BAT_POWER = 0x08

		self.REGION_RIGHT_KEYBOARD = 0x0001
		self.REGION_MIDDLE_RIGHT_KEYBOARD = 0x0002
		self.REGION_LEFT_KEYBOARD = 0x0008
		self.REGION_MIDDLE_LEFT_KEYBOARD = 0x0004
		self.REGION_POWER_BUTTON_2 = 0x0010
		self.REGION_RIGHT_SPEAKER = 0x0020
		self.REGION_LEFT_SPEAKER = 0x0040
		self.REGION_ALIEN_HEAD = 0x0080
		self.REGION_ALIEN_NAME = 0x0100
		self.REGION_TOUCH_PAD = 0x0200
		self.REGION_MEDIA_BAR = 0x1c00
		self.REGION_POWER_BUTTON = 0x2000
		self.REGION_POWER_BUTTON_EYES = 0x4000
		self.REGION_ALL_BUT_POWER = 0x0f9fff

		self.suportedMode["normal"] = AlienFXPowerMode(self.AlienFXProperties.ALIEN_FX_DEFAULT_POWER_MODE,self.AlienFXProperties.ALIEN_FX_DEFAULT_POWER_MODE, self.BLOCK_LOAD_ON_BOOT)
		self.suportedMode["standby"] = AlienFXPowerMode(self.AlienFXProperties.STANDBY_ID, self.AlienFXTexts.STAND_BY_DESCRIPTION, self.BLOCK_STANDBY)
		self.suportedMode["acPower"] = AlienFXPowerMode(self.AlienFXProperties.AC_POWER_ID, self.AlienFXTexts.AC_POWER_DESCRIPTION, self.BLOCK_AC_POWER)
		self.suportedMode["charging"] = AlienFXPowerMode(self.AlienFXProperties.CHARGING_ID, self.AlienFXTexts.CHARGING2_DESCRIPTION, self.BLOCK_CHARGING)
		self.suportedMode["onBat"] = AlienFXPowerMode(self.AlienFXProperties.ON_BATTERY_ID, self.AlienFXTexts.ON_BATTERY_DESCRIPTION, self.BLOCK_BAT_POWER)


		self.regions[self.AlienFXProperties.RIGHT_KEYBOARD_ID] = AlienFXRegion(self.AlienFXProperties.RIGHT_KEYBOARD_ID,  self.AlienFXTexts.RIGHT_KEYBOARD_DESCRIPTION, self.REGION_RIGHT_KEYBOARD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.RIGHT_CENTER_KEYBOARD_ID] = AlienFXRegion(self.AlienFXProperties.RIGHT_CENTER_KEYBOARD_ID, self.AlienFXTexts.RIGHT_CENTER_KEYBOARD_DESCRIPTION, self.REGION_MIDDLE_RIGHT_KEYBOARD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.LEFT_KEYBOARD_ID] = AlienFXRegion(self.AlienFXProperties.LEFT_KEYBOARD_ID,  self.AlienFXTexts.LEFT_KEYBOARD_DESCRIPTION, self.REGION_LEFT_KEYBOARD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.LEFT_CENTER_KEYBOARD_ID] = AlienFXRegion(self.AlienFXProperties.LEFT_CENTER_KEYBOARD_ID, self.AlienFXTexts.LEFT_CENTER_KEYBOARD_DESCRIPTION, self.REGION_MIDDLE_LEFT_KEYBOARD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.RIGHT_SPEAKER_ID] = AlienFXRegion(self.AlienFXProperties.RIGHT_SPEAKER_ID,  self.AlienFXTexts.RIGHT_SPEAKER_DESCRIPTION, self.REGION_RIGHT_SPEAKER,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.LEFT_SPEAKER_ID] = AlienFXRegion(self.AlienFXProperties.LEFT_SPEAKER_ID,  self.AlienFXTexts.LEFT_SPEAKER_DESCRIPTION, self.REGION_LEFT_SPEAKER,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.ALIEN_HEAD_ID] = AlienFXRegion(self.AlienFXProperties.ALIEN_HEAD_ID,  self.AlienFXTexts.ALIENWARE_HEAD_DESCRIPTION, self.REGION_ALIEN_HEAD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.ALIEN_LOGO_ID] = AlienFXRegion(self.AlienFXProperties.ALIEN_LOGO_ID,  self.AlienFXTexts.ALIENWARE_LOGO_DESCRIPTION, self.REGION_ALIEN_NAME,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.TOUCH_PAD_ID] = AlienFXRegion(self.AlienFXProperties.TOUCH_PAD_ID,  self.AlienFXTexts.TOUCHPAD_DESCRIPTION, self.REGION_TOUCH_PAD,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.MEDIA_BAR_ID] = AlienFXRegion(self.AlienFXProperties.MEDIA_BAR_ID,  self.AlienFXTexts.MEDIA_BAR_DESCRIPTION, self.REGION_MEDIA_BAR,self.SUPPORTED_COMMANDS,True,True,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.POWER_BUTTON_EYES_ID] = AlienFXRegion(self.AlienFXProperties.POWER_BUTTON_EYES_ID, self.AlienFXTexts.ALIENWARE_POWERBUTTON_EYES_DESCRIPTION, self.REGION_POWER_BUTTON_EYES,1,False,False,True, self.default_color , self.suportedMode)
		self.regions[self.AlienFXProperties.POWER_BUTTON_ID] = AlienFXRegion(self.AlienFXProperties.POWER_BUTTON_ID, self.AlienFXTexts.POWER_BUTTON_DESCRIPTION, self.REGION_POWER_BUTTON,2,True,True,True, self.default_color , self.suportedMode, power_button = True)

#added by SuperTool (end)
##############################################################################################

class AlienFXComputer:
	def __init__(self,name,vendorId,productId,computer):
		self.name = name
		self.vendorId = vendorId
		self.productId = productId
		self.computer = computer

class AllComputers():
	#Define General Device controls
	ALIENFX_USER_CONTROLS = 0x01
	ALIENFX_SLEEP_LIGHTS = 0x02
	ALIENFX_ALL_OFF = 0x03
	ALIENFX_ALL_ON = 0x04

	ALIENFX_MORPH = 0x01
	ALIENFX_BLINK = 0x02
	ALIENFX_STAY = 0x03
	ALIENFX_BATTERY_STATE = 0x0F

	ALIENFX_TOUCHPAD        = 0x000001
	ALIENFX_LIGHTPIPE       = 0x000020
	ALIENFX_ALIENWARE_LOGO  = 0x000080
	ALIENFX_ALIENHEAD       = 0x000100
	ALIENFX_POWER_BUTTON    = 0x008000
	ALIENFX_TOUCH_PANEL     = 0x010000

	ALIENFX_DEVICE_RESET = 0x06
	ALIENFX_READY = 0x10
	ALIENFX_BUSY = 0x11
	ALIENFX_UNKOWN_COMMAND = 0x12
	
	computerList = {
	"M11XR3" : AlienFXComputer("M11XR3",0x187c,0x0522,M11XR3()),
	"M11XR25" : AlienFXComputer("M11XR25", 0x187c,0x0516,M11XR3()),
	"M11XR2" : AlienFXComputer("M11XR2", 0x187c,0x0515,M11XR3()),
	"M11XR1" : AlienFXComputer("M11XR1", 0x187c,0x0514,M11XR3()),
	"M15XAllPowerful" : AlienFXComputer("M15XAllPowerful", 0x187c,0x0512,M15XAllPowerfull()),
	"M15XArea51" : AlienFXComputer("M15XArea51", 0x187c,0x0511,M15XArea51()),
	#############################################################################
	#added by niai (start)
	"M17XR3"	: AlienFXComputer("M17XR3", 0x187c,0x0520,M17XR3()),
	#added by niai (end)
	############################################################################
	#LightHash [start]
	"M14XR1" : AlienFXComputer("M14XR1", 0x187c,0x0521,M14XLight()),
	#"M14XR1" : AlienFXComputer("M14XR1",0x187c,0x0522,M14XLight())}
	#############################################################################
	#added by SuperTool (start)
	"M18XR2"	: AlienFXComputer("M18XR2", 0x187c,0x0518,M18XR2())}
	#added by SuperTool (end)
	############################################################################
	#LightHash [end]

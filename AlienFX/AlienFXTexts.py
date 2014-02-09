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

class AlienFXTexts:
	def __init__(self):
		#errors:
		self.ALIEN_FX_ERROR_TITLE_TEXT = "AlienFX error"
		self.DATA_LENGTH_ERROR_FORMAT = "Data length should be %d but was %d"
		self.DEVICE_NOT_PRESENT_ERROR_TEXT = "The application was unable to communicate with the alienFX device. The device is either not present, or the application lacks sufficient rights to access the device"
		self.COMMUNICATION_ERROR_FORMAT = "Error occured while trying to communicate with the AlienFX device: %s\n"
		self.DEVICE_PERMISSION_ERROR_TEXT = "The Device was found, but the application was unable to communicate with the alienFX controller. Do you have the right to access the alienfx device(e.g. are you running as admin)"
		self.SYSTEM_UI_NOT_FOUND = "System UI not Found"
		self.PROFILE_EXISTS_ERROR_TEXT = "Profile with that name already exists"
		self.PROFILE_NAME_EMPTY_ERROR_TEXT = "Name cannot be empty"
		self.SAVE_PROFILE_ERROR_FORMAT = "Failed to save the Profile: %s\n"
		self.ALREADY_RUNNING_ERROR_TEXT = "AlienFX is already running"
		
		#warnings
		self.ALIEN_FX_WARNING_TITLE_TEXT = "AlienFX Warning"
		self.SYSTEM_TRAY_WARNING_TEXT = "It seems the system does not support system trays. The Application will not run in background."
		
		#info messages
		self.ALIEN_FX_INFO_TITLE_TEXT = "AlienFx Info"
		self.SHOW_ALIEN_FX_LITE_TEXT = "Show AlienFXLite"
		self.ALIEN_FX_BACKGROUND_TEXT = "Still running in the background"
		self.ENTER_NAME_TITLE_TEXT = "Enter Name"
		self.ENTER_NAME_TEXT = "Enter a name for the new profile"
		self.USAGE_TITLE = "Usage"
		self.USAGE = "The Application is very similar in use as the AlienFX application developed by Alienware. \nFirst, create a new profile. Then you can select the colors for the given regions of your computer. \nAdding an action (Color, Blink, Morph) is done by pressing one of the small dropdown buttons.\nTo copy paste a given sequence of actions, just select the actions by pressing on the section they are in, and drag the mouse over them.\n Additionally, one can use modifiers such as shift and control to modify the way in which selection behaves. \nTo paste the selected section, click on the add button and then select the paste icon (the last one).\n Additionally, one can easily change the colors of profile by selecting a new color and pressing on a color in the Color used panel.\n This will change all actions with the color pressed on, to the selected color. \nPressing with the right mouse button on any color button or action will result in selecting that color.\nFinally, if you get weird behaviour, reset the AlienFX device by pressing on the Reset button under the help menu"
		self.ABOUT_FORMAT = "AlienFX Lite %s developed by %s"
		self.ABOUT_TITLE = "About"
		self.HELP_TITLE = "Help"
		self.RESET_TITLE = "Reset AlienFx"
		
		
		#Events
		self.EVENT_TURN_OFF_ALL = "Turn off AlienFX"
		self.EVENT_TURN_OFF_ALL_BUT_KEYBOARD = "Turn off All but Keyboard"
		self.EVENT_TURN_OFF_KEYBOARD = "Turn off keyboard"
		
		#controls
		self.EXIT_TEXT = "Exit"
		self.PREVIEW_LABEL_TEXT = "Preview"
		self.SELECT_PROFILE_TEXT = "Please select a profile from the combobox or create a new one"
		
		self.APPLY_THE_CURRENT_PROFILE = "Apply the current Profile"
		self.DELETE_THE_CURRENT_PROFILE = "Delete the current Profile"
		self.SAVE_THE_CURRENT_PROFILE = "Save the current Profile"
		self.CREATE_A_NEW_PROFILE = "Create a new Profile"
		self.PREVIEW_TOOL_TIP = "Preview Colors on AlienFX"
		
		self.PROFILE_SPEED_TEXT = "Speed:"
		self.COLORS_PROFILE_TITLE = "Colors Used in Profile"
		self.DEFAULT_TEXT = "Default"
		self.COLORS_TEXT = "Colors"
		self.PROFILE_TEXT = "Profile"
		
		self.PROFILE_SPEED_SLOW = "Slow"
		self.PROFILE_SPEED_FAST = "Fast"
		
		self.ACTION_COLOR_TEXT = "Color"
		self.ACTION_BLINK_TEXT = "Blink"
		self.ACTION_MORPH_TEXT = "Morph"
		

		self.DEFAULT_PROFILE_TEXT = "Default Profile"
		
		#Alienware devices:
		self.POWER_BUTTON_DESCRIPTION = "Power Button"
		self.ALIENWARE_POWERBUTTON_EYES_DESCRIPTION = "Powerbutton Eyes"
		self.MEDIA_BAR_DESCRIPTION = "Media Bar"
		self.TOUCHPAD_DESCRIPTION = "Touchpad"
		self.ALIENWARE_LOGO_DESCRIPTION = "Alienware logo"
		self.ALIENWARE_HEAD_DESCRIPTION = "Alienware head"
		self.LEFT_SPEAKER_DESCRIPTION = "Left Speaker"
		self.RIGHT_SPEAKER_DESCRIPTION = "Right Speaker"
		self.LEFT_CENTER_KEYBOARD_DESCRIPTION = "Left Center Keyboard"
		self.LEFT_KEYBOARD_DESCRIPTION = "Left Keyboard"
		self.RIGHT_CENTER_KEYBOARD_DESCRIPTION = "Right Center Keyboard"
		self.RIGHT_KEYBOARD_DESCRIPTION = "Right Keyboard"
		self.KEYBOARD_DESCRIPTION = "Keyboard"
		self.LIGHT_PIPE_DESCRIPTION = "Light Pipe"

		self.STEALTH_MODE_DESCRIPTION = "Stealth Mode"
		self.LID_CLOSED_DESCRIPTION = "Closed Lid"
		self.ON_BATTERY_DESCRIPTION = "On Battery"
		self.CHARGING2_DESCRIPTION = "Charging"
		self.AC_POWER_DESCRIPTION = "AC Power"
		self.STAND_BY_DESCRIPTION = "StandBy"

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

from AlienFX.AlienFXEngine import *
from AlienFX.AlienFXConfiguration import *
import pygtk
#pygtk.require("2.0")
import gtk, gobject
import cairo

from socket import *
from time import time
from time import sleep

#from gi.repository import Gtk as gtk
#from gi.repository import Gdk as gdk
#from gi.repository import GObject as gobject

gobject.threads_init()  

class pyAlienFX_GUI():
	def __init__(self):
		print "Initializing Driver  ..."
		self.driver = AlienFX_Driver()
		print "Initializing Controller ..."
		Deamon = Daemon_Controller()
		conn = Deamon.makeConnection()
		if not conn:
			self.controller = AlienFX_Controller(self.driver)
		else:
			self.controller = Deamon
		self.configuration = AlienFXConfiguration()
		try:
			f = open(os.path.join('.','Profiles',"last"),'r')
			profile = f.readline().strip()
		except:
			profile = "Default.cfg"
			#self.New_Conf(path=os.path.join('.','Profiles',profile))
		self.actual_conf_file = os.path.join('.','Profiles',profile)
		self.computer = self.driver.computer
		self.selected_area = None
		self.selected_mode = None
		self.selected_color1 = None
		self.selected_color2 = None
		self.lights = True
		#self.selected_speed = 0xc800
		self.selected_speed = 0xff00
		self.auto_apply = False
		self.default_color = "0000FF"
		self.selected_Id = 1
		self.background_color = "#222222"
		self.text_color = "#EEEEEE"
		self.set_color = 1
		self.Advanced_Mode = True
		self.width,self.height = 800,600
		self.Image_DB = Image_DB()
		if not os.path.isdir(os.path.join('.','Profiles')):
			os.mkdir(os.path.join('.','Profiles'))
		if os.path.isfile(self.actual_conf_file):
			print "Loading : %s"%self.actual_conf_file
			self.configuration.Load(self.actual_conf_file)
			print "SPEED = ",self.configuration.speed
		else:
			self.configuration.Create(self.actual_conf_file.split('.')[0],self.computer.name,self.selected_speed,self.actual_conf_file)
			self.New_Conf(self.actual_conf_file)

	def main(self):
		"""Main process, thread creation and wait for the main windows closure !"""
		print "Initializing Interface ..."
		self.AlienFX_Main()
		self.Create_zones()
		self.Create_Line()
		if not self.Advanced_Mode:
			self.AlienFX_Inside_vBox.children()[2].hide()
		self.AlienFX_Color_Panel()
		gtk.gdk.threads_enter()
		gtk.main()
		gtk.gdk.threads_leave()

	def Check_profiles(self):
		DB_profiles = {}
		profiles = os.listdir('./Profiles/')
		#print profiles
		for profile in profiles:
			if not ".cfg" in profile:
				#print "REMOVED : ",profile
				profiles.remove(profile)
		for profile in profiles:
			try:
				conf = AlienFXConfiguration()
				conf.Load(os.path.join('.','Profiles',profile))
				if not conf.name in DB_profiles.keys():
					DB_profiles[conf.name] = profile
			except:
				#print "REMOVED : ",profile
				profiles.remove(profile)
		return DB_profiles
		
	#================================
	#GTK functions!
	#================================
	def AlienFX_Main(self):
		"Creating the gtk object, loading the main glade file"
		self.gtk_AlienFX_Main = gtk.Builder()
		self.gtk_AlienFX_Main.add_from_file('./glade/AlienFXMain.glade')
		#Loading elements !
		self.AlienFX_Main_Windows = self.gtk_AlienFX_Main.get_object("AlienFX_Main_Windows")
		self.AlienFX_Main_Eventbox = self.gtk_AlienFX_Main.get_object("AlienFX_Main_Eventbox")
		self.AlienFX_Main_vBox = self.gtk_AlienFX_Main.get_object("AlienFX_Main_vBox")
		self.AlienFX_Main_MenuBar = self.gtk_AlienFX_Main.get_object("AlienFX_Main_MenuBar")
		self.AlienFX_Inside_Eventbox = self.gtk_AlienFX_Main.get_object("AlienFX_Inside_Eventbox")
		self.AlienFX_Inside_vBox = self.gtk_AlienFX_Main.get_object("AlienFX_Inside_vBox")
		self.AlienFX_Selector_hBox = self.gtk_AlienFX_Main.get_object("AlienFX_Selector_hBox")
		self.AlienFX_Computer_Eventbox = self.gtk_AlienFX_Main.get_object("AlienFX_Computer_Eventbox")
		self.AlienFX_Color_Eventbox = self.gtk_AlienFX_Main.get_object("AlienFX_Color_Eventbox")
		self.AlienFX_Preview_Eventbox = self.gtk_AlienFX_Main.get_object("AlienFX_Preview_Eventbox")
		self.AlienFX_Configurator_Eventbox = self.gtk_AlienFX_Main.get_object("AlienFX_Configurator_Eventbox")
		self.AlienFX_Configurator_ScrollWindow = self.gtk_AlienFX_Main.get_object("AlienFX_Configurator_ScrollWindow")
		self.AlienFX_ColorSelection_Window = self.gtk_AlienFX_Main.get_object("AlienFX_ColorSelection_Window")
		self.AlienFX_ComputerName_Label = self.gtk_AlienFX_Main.get_object("AlienFX_ComputerName_Label")
		self.AlienFX_Advanced_Button = self.gtk_AlienFX_Main.get_object("AlienFX_Button_Advanced")
		self.AlienFX_ComputerName_EventBox = self.gtk_AlienFX_Main.get_object("AlienFX_ComputerName_EventBox")
		self.AlienFX_Profiles_Eventbox = self.gtk_AlienFX_Main.get_object("AlienFX_Profiles_Eventbox")
		self.AlienFX_Profile_Chooser_Eventbox = self.gtk_AlienFX_Main.get_object("AlienFX_Profile_Chooser_Eventbox")
		self.AlienFX_Choose_Profile_Name = self.gtk_AlienFX_Main.get_object("AlienFX_Choose_Profile_Name")
		self.AlienFX_Tempo_EventBox = self.gtk_AlienFX_Main.get_object("AlienFX_Tempo_EventBox")



		#Modification of the background and elements !
		pixbuf = gtk.gdk.pixbuf_new_from_file(self.Image_DB.AlienFX_Main_Eventbox)
		pixbuf = pixbuf.scale_simple(self.width, self.height, gtk.gdk.INTERP_BILINEAR)
		pixmap, mask = pixbuf.render_pixmap_and_mask()
		self.AlienFX_Main_Windows.set_app_paintable(True)
		self.AlienFX_Main_Windows.resize(self.width, self.height)
		self.AlienFX_Main_Windows.realize()
		self.AlienFX_Main_Windows.window.set_back_pixmap(pixmap, False)
		self.AlienFX_ComputerName_Label.set_label(self.computer.name)
		self.gtk_AlienFX_Main.connect_signals(self)
		
		
		#Background Colors !
		self.AlienFX_ComputerName_EventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
		self.AlienFX_ComputerName_Label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.text_color))
		self.AlienFX_Configurator_ScrollWindow.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
		self.AlienFX_Profiles_Eventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
		self.AlienFX_Profile_Chooser_Eventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
		self.AlienFX_Tempo_EventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
		#Optional to be deleted enventually !
		#====----====
		self.AlienFX_Color_Eventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
		self.AlienFX_Computer_Eventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
		self.AlienFX_Main_Eventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
		self.AlienFX_Configurator_Eventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
		#====----====

		#========Creation of different GTK elements not specified in Glade=========
		self.AlienFX_Tempo_VBox = gtk.VBox()
		self.AlienFX_Tempo_Label = gtk.Label()
		self.AlienFX_Tempo_Label.set_label(" Tempo ")
		self.AlienFX_Tempo_Label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.text_color))
		ajustement = gtk.Adjustment((self.configuration.speed/256), 1, 255, 1, 16)
		self.AlienFX_Tempo_Ruler = gtk.VScale(ajustement)
		self.AlienFX_Tempo_Ruler.set_size_request(-1,110)
		self.AlienFX_Tempo_Ruler.set_digits(0)
		self.AlienFX_Tempo_Ruler.set_draw_value(False)
		self.AlienFX_Tempo_Ruler.connect("change-value",self.on_AlienFX_Tempo_Changed)
		self.AlienFX_Tempo_EventBox.add(self.AlienFX_Tempo_VBox)
		#self.AlienFX_Tempo_Ruler.set_range(0, 255, 200, 255)
		self.AlienFX_Tempo_VBox.pack_start(self.AlienFX_Tempo_Label)
		self.AlienFX_Tempo_VBox.pack_start(self.AlienFX_Tempo_Ruler)
		Apply = gtk.Button()
		Apply.set_label("Preview")
		Apply.connect("clicked",self.on_Apply_pressed)
		Save = gtk.Button()
		Save.set_label("Save")
		Save.connect("clicked",self.on_Save_pressed)
		box = gtk.VBox()
		box.pack_start(Apply)
		box.pack_start(Save)
		self.Updtate_Profile_Combobox()
		self.AlienFX_Computer_Eventbox.add(box)
		self.on_Advanced_Button_Clicked(self.AlienFX_Advanced_Button)

	def Updtate_Profile_Combobox(self):
		#print "Updating Profiles"
		try:
			self.AlienFX_Profiles_Combobox.destroy()
		except:
			pass
		self.AlienFX_Profiles_Combobox = gtk.combo_box_new_text()
		self.Profiles = self.Check_profiles()
		self.Profiles_Positions = {}
		n = 0
		for p in self.Profiles.keys():
			self.Profiles_Positions[self.Profiles[p]] = n
			self.AlienFX_Profiles_Combobox.append_text(p)
			n += 1
		#print self.actual_conf_file.split('/')[-1]
		#print self.Profiles_Positions.keys()
		if self.actual_conf_file.split('/')[-1] in self.Profiles_Positions.keys():
			#print "set Active"
			self.AlienFX_Profiles_Combobox.set_active(self.Profiles_Positions[self.actual_conf_file.split('/')[-1]])
		try:
			self.AlienFX_Profiles_Eventbox.add(self.AlienFX_Profiles_Combobox)
			self.AlienFX_Profiles_Combobox.connect("changed",self.on_Profile_changed)
			self.AlienFX_Profiles_Combobox.show_all()
		except:
			pass


	def Create_Border(self,Type,Inside,Label = None,zone=None ,confId=None):
		"""2 type of border Advanced (type == 1) and Normal (type == 0)
		That function creates the gtk Box that contains the images border that surround the zones."""
		if Type == 0:
			MainBox = gtk.VBox()
			TopBox = gtk.HBox()
			MiddleBox = gtk.HBox()
			BottomBox = gtk.HBox()
			TopBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
			UL = gtk.EventBox()
			ULi = gtk.Image()
			ULi.set_from_file(self.Image_DB.AlienFX_Cadre_0_Up_Left)
			UL.add(ULi)
			UL.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
			UL2 = gtk.EventBox()
			UL2i = gtk.Image()
			UL2i.set_from_file(self.Image_DB.AlienFX_Cadre_0_Up_Left2)
			UL2.add(UL2i)
			UL2.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
			if len(Label)<11:
				Title_width = (11)*9
			else:
				Title_width = (len(Label)*9)
			UMbg = gtk.gdk.pixbuf_new_from_file_at_scale(self.Image_DB.AlienFX_Cadre_0_Up_Middle,width=Title_width,height=31,preserve_aspect_ratio=False)
			#print "LEN ======>>>>>%s >> %s"%(Label,Title_width)
			UM = gtk.EventBox()
			UM.set_size_request(width=Title_width,height=-1)
			UM.connect('expose_event', self.__textbackground, UMbg)
			text = gtk.Label('<span size="11000" color="#00FFFF">%s</span>'%Label)
			text.set_use_markup(gtk.TRUE)
			UM.add(text)
			UM.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
			UR = gtk.EventBox()
			URi = gtk.Image()
			URi.set_from_file(self.Image_DB.AlienFX_Cadre_0_Up_Right)
			UR.add(URi)
			UR.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
			UR2 = gtk.EventBox()
			UR2i = gtk.Image()
			UR2i.set_from_file(self.Image_DB.AlienFX_Cadre_0_Up_Right2)
			UR2.add(UR2i)
			UR2.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
			L = gtk.EventBox()
			Li = gtk.Image()
			Li.set_from_file(self.Image_DB.AlienFX_Cadre_0_Left)
			L.add(Li)
			L.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
			R = gtk.EventBox()
			Ri = gtk.Image()
			Ri.set_from_file(self.Image_DB.AlienFX_Cadre_0_Right)
			R.add(Ri)
			R.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
			BL = gtk.EventBox()
			BLi = gtk.Image()
			BLi.set_from_file(self.Image_DB.AlienFX_Cadre_0_Bottom_Left)
			BL.add(BLi)
			BL.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
			BL2 = gtk.EventBox()
			BL2i = gtk.Image()
			BL2i.set_from_file(self.Image_DB.AlienFX_Cadre_0_Bottom_Middle_Left)
			BL2.add(BL2i)
			BL2.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
			BM = gtk.EventBox()
			BMi = gtk.Image()
			BMbg = gtk.gdk.pixbuf_new_from_file_at_scale(self.Image_DB.AlienFX_Cadre_0_Bottom_Middle,width=((81+Title_width)-165),height=16,preserve_aspect_ratio=False)
			BMi.set_from_pixbuf(BMbg)
			BMi.set_size_request(width=((81+Title_width)-165),height=-1)
			BM.add(BMi)
			BM.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
			BR2 = gtk.EventBox()
			BR2i = gtk.Image()
			BR2i.set_from_file(self.Image_DB.AlienFX_Cadre_0_Bottom_Middle_Right)
			BR2.add(BR2i)
			BR2.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
			BR = gtk.EventBox()
			BRi = gtk.Image()
			BRi.set_from_file(self.Image_DB.AlienFX_Cadre_0_Bottom_Right)
			BR.add(BRi)
			BR.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
			Inside.set_size_request(width = (81+Title_width)- 33,height=-1)
			TopBox.pack_start(UL,gtk.SHRINK)
			TopBox.pack_start(UL2,gtk.SHRINK)
			TopBox.pack_start(UM,gtk.SHRINK)
			TopBox.pack_start(UR2,gtk.SHRINK)
			TopBox.pack_start(UR,gtk.SHRINK)
			MiddleBox.pack_start(L,gtk.SHRINK)
			MiddleBox.pack_start(Inside,gtk.SHRINK)
			MiddleBox.pack_start(R,gtk.SHRINK)
			BottomBox.pack_start(BL,gtk.SHRINK)
			BottomBox.pack_start(BL2,gtk.SHRINK)
			BottomBox.pack_start(BM,gtk.SHRINK)
			BottomBox.pack_start(BR2,gtk.SHRINK)
			BottomBox.pack_start(BR,gtk.SHRINK)
			MainBox.pack_start(TopBox,gtk.SHRINK)
			MainBox.pack_start(MiddleBox,gtk.SHRINK)
			MainBox.pack_start(BottomBox,gtk.SHRINK)
			return MainBox
		elif Type == 1:
			MainBox = gtk.VBox(spacing=0,homogeneous=False)
			TopBox = gtk.HBox(spacing=0,homogeneous=False)
			MiddleBox = gtk.HBox(spacing=0,homogeneous=False)
			BottomBox = gtk.HBox(spacing=0,homogeneous=False)
			UL = gtk.Image()
			UL.set_from_file(self.Image_DB.AlienFX_Cadre_01_Up_Left)
			UM = gtk.Image()
			UM.set_from_file(self.Image_DB.AlienFX_Cadre_01_Up_Middle)
			UR = gtk.EventBox()
			UR.set_above_child(True)
			UR.connect("button-press-event",self.on_Remove_Clicked,zone,confId)
			UR.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
			URi = gtk.Image()
			URi.set_from_file(self.Image_DB.AlienFX_Cadre_01_Up_Right_c)
			UR.add(URi)
			L = gtk.Image()
			L.set_from_file(self.Image_DB.AlienFX_Cadre_01_Left)
			R = gtk.Image()
			R.set_from_file(self.Image_DB.AlienFX_Cadre_01_Right)
			BL = gtk.Image()
			BL.set_from_file(self.Image_DB.AlienFX_Cadre_01_Bottom_Left)
			BM = gtk.Image()
			BM.set_from_file(self.Image_DB.AlienFX_Cadre_01_Bottom_Middle)
			BR = gtk.Image()
			BR.set_from_file(self.Image_DB.AlienFX_Cadre_01_Bottom_Right)
			TopBox.pack_start(UL,gtk.SHRINK)
			TopBox.pack_start(UM,gtk.SHRINK)
			TopBox.pack_start(UR,gtk.SHRINK)
			MiddleBox.pack_start(L,gtk.SHRINK)
			MiddleBox.pack_start(Inside,gtk.SHRINK)
			MiddleBox.pack_start(R,gtk.SHRINK)
			BottomBox.pack_start(BL,gtk.SHRINK)
			BottomBox.pack_start(BM,gtk.SHRINK)
			BottomBox.pack_start(BR,gtk.SHRINK)
			TopBox.set_size_request(180,-1)
			MiddleBox.set_size_request(180,-1)
			BottomBox.set_size_request(180,-1)
			MainBox.set_size_request(180,-1)
			MainBox.pack_start(TopBox)
			MainBox.pack_start(MiddleBox)
			MainBox.pack_start(BottomBox)
			return MainBox
		elif Type == 2:
			MainBox = gtk.VBox(spacing=0,homogeneous=False)
			TopBox = gtk.HBox(spacing=0,homogeneous=False)
			MiddleBox = gtk.HBox(spacing=0,homogeneous=False)
			BottomBox = gtk.HBox(spacing=0,homogeneous=False)
			UL = gtk.Image()
			UL.set_from_file(self.Image_DB.AlienFX_Cadre_02_Up_Left)
			UM = gtk.Image()
			UM.set_from_file(self.Image_DB.AlienFX_Cadre_02_Up_Middle)
			UR = gtk.Image()
			UR.set_from_file(self.Image_DB.AlienFX_Cadre_02_Up_Right)
			L = gtk.Image()
			L.set_from_file(self.Image_DB.AlienFX_Cadre_02_Left)
			R = gtk.Image()
			R.set_from_file(self.Image_DB.AlienFX_Cadre_02_Right)
			BL = gtk.Image()
			BL.set_from_file(self.Image_DB.AlienFX_Cadre_02_Bottom_Left)
			BM = gtk.Image()
			BM.set_from_file(self.Image_DB.AlienFX_Cadre_02_Bottom_Middle)
			BR = gtk.Image()
			BR.set_from_file(self.Image_DB.AlienFX_Cadre_02_Bottom_Right)
			TopBox.pack_start(UL,gtk.SHRINK)
			TopBox.pack_start(UM,gtk.SHRINK)
			TopBox.pack_start(UR,gtk.SHRINK)
			MiddleBox.pack_start(L,gtk.SHRINK)
			MiddleBox.pack_start(Inside,gtk.SHRINK)
			MiddleBox.pack_start(R,gtk.SHRINK)
			BottomBox.pack_start(BL,gtk.SHRINK)
			BottomBox.pack_start(BM,gtk.SHRINK)
			BottomBox.pack_start(BR,gtk.SHRINK)
			#TopBox.set_size_request(40,-1)
			#MiddleBox.set_size_request(40,-1)
			#BottomBox.set_size_request(40,-1)
			#MainBox.set_size_request(40,40)
			MainBox.pack_start(TopBox, gtk.SHRINK)
			MainBox.pack_start(MiddleBox, gtk.SHRINK)
			MainBox.pack_start(BottomBox, gtk.SHRINK)
			return MainBox
		return Inside

	def gradient_box(self, width, height, color1, color2, power):
		#color1 = [122,255,22]
		#color2 = [255,34,122]
		#color1 = self.norm_color(color1)
		#color2 = self.norm_color(color2)
		cm = self.color_mean(color1,color2)
		darea1 = gtk.DrawingArea()
		if power:
			cm = color1
		darea1.connect("expose-event", self.expose_gradient,1,color1,color2,cm,width)
		darea2 = gtk.DrawingArea()
		if power:
			cm = color2
		darea2.connect("expose-event", self.expose_gradient,2,color1,color2,cm,width)
		return darea1,darea2

	def color_mean(self, color1, color2):
		cf = [0,0,0]
		cf[0] = ((color1[0] + color2[0])/2.0)
		cf[1] = ((color1[1] + color2[1])/2.0)
		cf[2] = ((color1[2] + color2[2])/2.0)
		#print "Color1 : %s\nColor2 : %s\nColor F : %s"%(color1,color2,cf)
		return cf

	def norm_color(self,color):
		doit = False
		for i in color:
			if i > 1:
				doit = True
		for i in range(0,len(color)):
			color[i] = color[i]/255.0
		return color


	def expose_gradient(self, widget, event, zone, color1, color2, cm, width):
		#print "Exposing the gradient on Eventbox : ",widget
		if zone == 1:
			start = color1
			stop = cm
		if zone == 2:
			start = cm
			stop = color2
		#Creating the PixBuf object !
		#cspace = gtk.gdk.Colorspace(0)
		#pixbuf = gtk.gdk.Pixbuf(cspace,False,8,width,100)
		#pixbuf_width = pixbuf.get_width()
		#pixbuf_height = pixbuf.get_height()
		#pix_data = pixbuf.get_pixels_array()
		#print len(pix_data)
		#print pixbuf_width
		#print len(pix_data[0])
		#print pixbuf_height
		#Creating the Cairo object!
		#surface = cairo.ImageSurface.create_for_data(pix_data, cairo.FORMAT_RGB24, pixbuf.get_width(), pixbuf.get_height(), pixbuf.get_rowstride())
		#stride = cairo.ImageSurface.format_stride_for_width(cspace, pixbuf_width)
		#print stride
		#surface = cairo.ImageSurface.create_for_data(pix_data, cspace, pixbuf_width, pixbuf_height ,stride)
		#cr = cairo.Context(surface)
		#cr.save()
		#cr.scale(1.0, 1.0)

		cr = widget.window.cairo_create()
		#Drawinf the gradient !
		lg1 = cairo.LinearGradient(0.0, 0.0, width, 0)
		lg1.add_color_stop_rgb(0, start[0], start[1], start[2])
		lg1.add_color_stop_rgb(1, stop[0], stop[1], stop[2])
		cr.rectangle(0, 0, width, 100)
		cr.set_source(lg1)
		cr.fill()
		#cr.save()
		#cr.restore()
		#surface.flush()
		#surface.finish()
		#print cr
		#widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL],cr, 0, 0, 0, 0)
		#if widget.get_child() != None:
			#widget.propagate_expose(widget.get_child(), ev)
		return True

	def Create_zones(self):
		"""That function creates a gtk object.
		That object is the Normal Selections boxes (not advanced).
		It calls self.Widget_Zone that is the boxes unit creator"""
		#print "Advanced mode : ",self.Advanced_Mode
		try:
			self.AlienFX_Preview_Hbox.destroy()
			#print "Destroy"
		except:
			pass
		if self.Advanced_Mode == False:
			self.AlienFX_Preview_Hbox = gtk.HBox()
			self.AlienFX_Preview_Hbox.set_spacing(20)
			for zone in self.computer.regions.keys():
				self.AlienFX_Preview_Hbox.pack_start(self.Widget_Zone(self.computer.regions[zone]), expand=False)
			self.AlienFX_Preview_Eventbox.add(self.AlienFX_Preview_Hbox)
			self.AlienFX_Preview_Eventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
			self.AlienFX_Main_Windows.show_all()
	
	def Widget_Zone(self,zone,confId = 0,line = False):
		"""That function creates a gtk object.
		This object is a not advanced zone box"""
		#print "Creating : ",zone.description
		Zone_VBox = gtk.VBox(False)
		set_type = 1
		Label = None
		height = 40
		if not zone.power_button:
			width = (180-33-28)/2
		else:
			width = (180-33)/2
		if not line:
			set_type = 0
			Label = zone.description
			if len(Label)<11:
				Title_width = (11)*9
			else:
				Title_width = (len(Label)*9)
			if not zone.power_button:
				width = ((81+Title_width)- 33 -28)/2
			else:
				width = ((81+Title_width)- 33)/2
			#title = gtk.Label(zone.description)
			#Zone_VBox.pack_start(title, expand=False)
		#color = gtk.EventBox()
		#color_hbox = gtk.HBox()
		
		#color_hbox.pack_start(color2)
		#print self.configuration.Show_Configuration()
		c1 = gtk.gdk.Color('#'+self.configuration.area[zone.name][confId].color1)
		if zone.power_button:
			c2 = gtk.gdk.Color('#'+self.configuration.area[zone.name][confId].color2)
		elif self.configuration.area[zone.name][confId].mode != "morph":
			c2 = gtk.gdk.Color('#'+self.configuration.area[zone.name][confId].color1)
		else:
			c2 = gtk.gdk.Color('#'+self.configuration.area[zone.name][confId].color2)

		grad1,grad2 = self.gradient_box(width,height,[c1.red_float,c1.green_float,c1.blue_float],[c2.red_float,c2.green_float,c2.blue_float],zone.power_button)
		cm = self.color_mean([c1.red_float,c1.green_float,c1.blue_float],[c2.red_float,c2.green_float,c2.blue_float])
		#darea1 = gtk.DrawingArea()
		#darea2 = gtk.DrawingArea()
		#darea2.connect("expose-event", self.expose_gradient,2,color1,color2,cm,width)
		#return darea1,darea2

		color1 = gtk.EventBox()
		#color1.connect("expose-event", self.expose_gradient,1,[c1.red_float,c1.green_float,c1.blue_float],[c2.red_float,c2.green_float,c2.blue_float],cm,width)
		color1.add(grad1)
		color1.set_above_child(True)
		color1.set_size_request(width, -1)
		color1.connect("button-press-event", self.on_AlienFX_Preview_Zone_Clicked , zone, confId, 1)
		#color1.connect("enter-notify-event", self.on_color_focus_in, zone, confId)
		#color1.connect("leave-notify-event", self.on_color_focus_out, zone, confId)

		color2 = gtk.EventBox()
		color2.add(grad2)
		#color2.connect("expose-event", self.expose_gradient,2,[c1.red_float,c1.green_float,c1.blue_float],[c2.red_float,c2.green_float,c2.blue_float],cm,width)
		color2.set_above_child(True)
		color2.set_size_request(width, -1)
		color2.connect("button-press-event", self.on_AlienFX_Preview_Zone_Clicked , zone, confId, 2)
		#color2.connect("enter-notify-event", self.on_color_focus_in, zone, confId)
		#color2.connect("leave-notify-event", self.on_color_focus_out, zone, confId)


		#color_hbox.pack_start(color1)
		mode = gtk.VBox()
		if not zone.power_button:
			if self.configuration.area[zone.name][confId].mode == "fixed":
				if zone.canLight:
					image1 = self.Image_DB.AlienFX_Icon_Fixed_On
				if zone.canBlink:
					image2 = self.Image_DB.AlienFX_Icon_Blink_Off
				if zone.canMorph:
					image3 = self.Image_DB.AlienFX_Icon_Morph_Off
			elif self.configuration.area[zone.name][confId].mode == "blink":
				if zone.canLight:
					image1 = self.Image_DB.AlienFX_Icon_Fixed_Off
				if zone.canBlink:
					image2 = self.Image_DB.AlienFX_Icon_Blink_On
				if zone.canMorph:
					image3 = self.Image_DB.AlienFX_Icon_Morph_Off
			elif self.configuration.area[zone.name][confId].mode == "morph":
				if zone.canLight:
					image1 = self.Image_DB.AlienFX_Icon_Fixed_Off
				if zone.canBlink:
					image2 = self.Image_DB.AlienFX_Icon_Blink_Off
				if zone.canMorph:
					image3 = self.Image_DB.AlienFX_Icon_Morph_On
			if zone.canLight:
				fixed = gtk.Image()
				fixed.set_from_file(image1)
				EventFixed = gtk.EventBox()
				EventFixed.add(fixed)
				EventFixed.connect("button-press-event", self.on_AlienFX_Preview_Mode_Clicked, "fixed", zone, confId)
				mode.pack_start(EventFixed, expand=False)
			if zone.canBlink:	
				blink = gtk.Image()
				blink.set_from_file(image2)
				EventBlink = gtk.EventBox()
				EventBlink.add(blink)
				EventBlink.connect("button-press-event", self.on_AlienFX_Preview_Mode_Clicked, "blink", zone, confId)
				mode.pack_start(EventBlink, expand=False)
			if zone.canMorph:
				morph = gtk.Image()
				morph.set_from_file(image3)
				EventMorph = gtk.EventBox()
				EventMorph.add(morph)
				EventMorph.connect("button-press-event", self.on_AlienFX_Preview_Mode_Clicked, "morph", zone, confId)
				mode.pack_start(EventMorph, expand=False)
		Color_Hbox = gtk.HBox()
		#Color_Hbox.set_spacing(20)
		Color_Hbox.pack_start(color1, expand=False)
		Color_Hbox.pack_start(color2, expand=False)
		Color_Hbox.pack_start(mode, expand=False)
		Table = self.Create_Border(set_type,Color_Hbox,Label,zone,confId)
		Zone_VBox.pack_start(Table, expand=False)
		return Zone_VBox
	
	def Create_Line(self):
		"""That function creates a gtk object.
		That object is the Normal Selections boxes (not advanced).
		It calls self.Widget_Zone that is the boxes creator"""
		#if self.Advanced_Mode == True:
		#print "Creating lines"
		#print "Advanced mode : ",self.Advanced_Mode
		try:
			self.AlienFX_Configurator_Table.destroy()
			self.AlienFX_Configurator_Eventbox.destroy()
			#print "Destroy"
		except:
			pass
		l = 1
		self.AlienFX_Configurator_Table = gtk.Table(len(self.computer.regions.keys()),l,True)
		self.AlienFX_Configurator_Table.set_row_spacings(20)
		self.AlienFX_Configurator_Table.set_col_spacings(20)
		old = 0
		for zone in self.configuration.area.keys():
			new = len(self.configuration.area[zone])
			old = max(old,new)
			self.AlienFX_Configurator_Table.resize(old+1,l)
			self.Widget_Line(self.computer.regions[zone],l)
			l += 1
		self.AlienFX_Configurator_Eventbox = gtk.EventBox()
		self.AlienFX_Configurator_Eventbox.add(self.AlienFX_Configurator_Table)
		self.AlienFX_Configurator_Eventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.background_color))
		self.AlienFX_Configurator_ScrollWindow.add_with_viewport(self.AlienFX_Configurator_Eventbox)
		self.AlienFX_Main_Windows.show_all()
	
	def Widget_Line(self, zone, l):
		"""That function creates a gtk object.
		This object is an advanced zone box"""
		#print "Creating : ",zone.description
		title = gtk.Label(zone.description)
		title.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.text_color))
		self.AlienFX_Configurator_Table.attach(title,0,1,l-1,l,xoptions=gtk.SHRINK)#,xoptions=gtk.EXPAND
		for conf in range(len(self.configuration.area[zone.name])):
			confBox = self.Widget_Zone(zone, conf, line=True)
			self.AlienFX_Configurator_Table.attach(confBox,int(conf)+1,int(conf)+2,l-1,l,xoptions=gtk.SHRINK,yoptions=gtk.SHRINK)
		if not zone.power_button:
			AddConf = gtk.Button()
			AddConf.set_label("Add")
			AddConf.connect("clicked", self.on_Line_AddConf_pressed, zone, conf)
			self.AlienFX_Configurator_Table.attach(AddConf,int(conf)+2,int(conf)+3,l-1,l,xoptions=gtk.SHRINK,yoptions=gtk.SHRINK)
		
	
	def Set_Conf(self,Save=False):
		Id = 0x00
		self.controller.Set_Loop_Conf(Save, self.computer.BLOCK_LOAD_ON_BOOT)
		self.controller.Add_Speed_Conf(self.selected_speed)
		max_conf = 1
		for zone in self.computer.regions.keys():
			if not self.computer.regions[zone].power_button:
				max_conf = max(max_conf,len(self.configuration.area[zone]))
		tmp = {}
		sorted_regions = []
		for r in self.computer.regions.keys():
			tmp[self.computer.regions[r].regionId] = r
		stmp = tmp.keys()
		stmp.sort()
		for k in stmp:
			sorted_regions.append(tmp[k])
		for zone in sorted_regions:
			if self.computer.regions[zone].power_button:
				power = zone
			Id += 0x01 
			if not self.computer.regions[zone].power_button:
				nb_conf = 0
				for conf in range(len(self.configuration.area[zone])):
					nb_conf += 1
					self.controller.Add_Loop_Conf(self.computer.regions[zone].regionId,self.configuration.area[zone][conf].mode,self.configuration.area[zone][conf].color1,self.configuration.area[zone][conf].color2)
				if len(self.configuration.area[zone]) != 1:
					while nb_conf != max_conf:
						nb_conf += 1
						conf = -1
						self.controller.Add_Loop_Conf(self.computer.regions[zone].regionId,self.configuration.area[zone][conf].mode,self.configuration.area[zone][conf].color1,self.configuration.area[zone][conf].color2)
				self.controller.End_Loop_Conf()
			#self.controller.Add_Loop_Conf(0x0f869e,"fixed",'000000','000000')
			#self.controller.End_Loop_Conf()
		#if not Save:
			#self.controller.Add_Loop_Conf(self.computer.REGION_ALL_BUT_POWER,"fixed","FF0000","00FF00")
			#self.controller.End_Loop_Conf()
		self.controller.End_Transfert_Conf()
		self.controller.Write_Conf()
		if Save:
			color1 = self.configuration.area[power][0].color1
			color2 = self.configuration.area[power][0].color2
			area = self.computer.regions[power].regionId
			#Block = 0x02 ! Sleeping Mode !!!!!

		
			self.controller.Set_Loop_Conf(Save,self.computer.BLOCK_STANDBY)
			self.controller.Add_Loop_Conf(area,"morph",color1,'000000')
			self.controller.Add_Loop_Conf(area,"morph",'000000',color1)
			self.controller.End_Loop_Conf()
			self.controller.Add_Loop_Conf(self.computer.REGION_ALL_BUT_POWER,"fixed",'000000')
			self.controller.End_Loop_Conf()
			self.controller.End_Transfert_Conf()
			self.controller.Write_Conf()

			#Block = 0x05 ! A/C powered !
			self.controller.Set_Loop_Conf(Save,self.computer.BLOCK_AC_POWER)
			self.controller.Add_Loop_Conf(area,"fixed",color1)
			self.controller.End_Loop_Conf()
			self.controller.End_Transfert_Conf()
			self.controller.Write_Conf()
			
			#Block = 0x06 ! Charging !
			self.controller.Set_Loop_Conf(Save,self.computer.BLOCK_CHARGING)
			self.controller.Add_Loop_Conf(area,"morph",color1,color2)
			self.controller.Add_Loop_Conf(area,"morph",color2,color1)
			self.controller.End_Loop_Conf()
			self.controller.End_Transfert_Conf()
			self.controller.Write_Conf()
			
			#Block 0x07 ! Battery Sleeping !
			self.controller.Set_Loop_Conf(Save,self.computer.BLOCK_BATT_SLEEPING)
			self.controller.Add_Loop_Conf(area,"morph",color2,'000000')
			self.controller.Add_Loop_Conf(area,"morph",'000000',color2)
			self.controller.End_Loop_Conf()
			self.controller.Add_Loop_Conf(self.computer.REGION_ALL_BUT_POWER,"fixed",'000000')
			self.controller.End_Loop_Conf()
			self.controller.End_Transfert_Conf()
			self.controller.Write_Conf()

			#Block 0x08 ! On Battery !
			self.controller.Set_Loop_Conf(Save,self.computer.BLOCK_BAT_POWER)
			self.controller.Add_Loop_Conf(area,"fixed",color2)
			self.controller.End_Loop_Conf()
			self.controller.End_Transfert_Conf()
			self.controller.Write_Conf()
			
			#Block 0x09 ! Critical When Sleeping ... 
			self.controller.Set_Loop_Conf(Save,self.computer.BLOCK_BATT_CRITICAL)
			self.controller.Add_Loop_Conf(area,"blink",color2)
			self.controller.End_Loop_Conf()
			self.controller.End_Transfert_Conf()
			self.controller.Write_Conf()
			
			#Applying after all the saving !
			self.Set_Conf()
		self.configuration.Save(path="default.cfg")
			
	def Select_Zone(self,zone):
		"""When a zone is selected, launch the correct functions"""
		pass
	
	def Set_color(self):
		if self.selected_mode == "fixed":
			self.controller.Set_Color(self.selected_area.regionId,self.selected_color1)
		if self.selected_mode == "blink":
			self.controller.Set_Color_Blink(self.selected_area.regionId,self.selected_color1)
		if self.selected_mode == "morph" and self.selected_color2:
			#print "\n\n\n",self.selected_color2
			self.controller.Set_Color_Morph(self.selected_area.regionId,self.selected_color1,self.selected_color2)
		
	
	def AlienFX_Color_Panel(self):
		default_color = ["FFFFFF","FFFF00","FF00FF","00FFFF","FF0000","00FF00","0000FF","000000","select"]
		self.AlienFX_Color_Panel_VBox = gtk.VBox(spacing = 5)
		HBox1 = gtk.HBox(spacing = 5)
		HBox2 = gtk.HBox(spacing = 5)
		n = 0
		for c in default_color:
			if c == "select":
				color_select_button = gtk.Button()
				color_select_button.set_label("Color Selector")
				color_select_button.connect("clicked", self.on_color_select_button_Clicked)
				self.AlienFX_Color_Panel_VBox.pack_start(color_select_button, expand=True)
			else:
				fixed = gtk.Fixed()
				color_EventBox = gtk.EventBox()
				color_EventBox.set_size_request(35,37)
				color_EventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('#'+c))
				color_EventBox.connect("button-press-event", self.on_AlienFX_Color_Panel_Clicked, c)
				fixed.add(color_EventBox)
				box = self.Create_Border(2,fixed)
				if n > 3:
					HBox2.pack_start(box, gtk.SHRINK)
				else:
					HBox1.pack_start(box, gtk.SHRINK)
				n += 1

		self.AlienFX_Color_Panel_VBox.pack_start(HBox2, gtk.SHRINK)
		self.AlienFX_Color_Panel_VBox.pack_start(HBox1, gtk.SHRINK)
		self.AlienFX_Color_Eventbox.add(self.AlienFX_Color_Panel_VBox)
		self.AlienFX_Main_Windows.show_all()

	def New_Conf(self,path = None):
		if not path:
			chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_SAVE,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
			filter = gtk.FileFilter()
			filter.set_name("Conf Files")
			filter.add_pattern("*.cfg")
			chooser.add_filter(filter)
			chooser.set_current_folder(os.path.join('.',"Profiles"))
			chooser.set_current_name(self.new_title+".cfg")
			response = chooser.run()
			if response == gtk.RESPONSE_OK:
				self.actual_conf_file = chooser.get_filename()
				if not ".cfg" in self.actual_conf_file:
					self.actual_conf_file = self.actual_conf_file + ".cfg"
				self.configuration = AlienFXConfiguration()
				self.configuration.Create(self.new_title,self.computer.name,self.selected_speed,self.actual_conf_file)
				chooser.destroy()
			elif response == gtk.RESPONSE_CANCEL:
				print 'Closed, no files selected'
				chooser.destroy()
				return False
		for zone in self.computer.regions.keys():
			self.configuration.Add(self.computer.regions[zone])
			self.configuration.area[zone].append(self.computer.default_mode,self.computer.default_color,self.computer.default_color)
			self.on_Configuration_Save("widget")
		self.Updtate_Profile_Combobox()
		#self.Create_zones()
		#self.Create_Line()
	
	
	#================================
	#Connect functions!
	#================================

	def on_New_Conf(self):
		self.AlienFX_Choose_Profile_Name.show_all()
	
	def on_AlienFX_Choose_Profile_Name_Button_clicked(self,widget):
		#print widget
		self.new_title = widget.get_text()
		self.AlienFX_Choose_Profile_Name.hide()
		self.New_Conf()
	
	def on_Profile_changed(self,widget,p = None):
		"""Get the profile selected and changes to that profile !"""
		if not p:
			choosed_profile = widget.get_active_text()
		else:
			choosed_profile = p
		#print choosed_profile,self.Profiles[choosed_profile],self.actual_conf_file
		if choosed_profile != self.actual_conf_file:
			self.actual_conf_file = os.path.join('.','Profiles',self.Profiles[choosed_profile])
			self.configuration = AlienFXConfiguration()
			self.configuration.Load(self.actual_conf_file)
			f = open(os.path.join('.','Profiles',"last"),'w')
			f.write(self.Profiles[choosed_profile])
			self.speed = self.configuration.speed
			self.AlienFX_Tempo_Ruler.set_value(int(self.speed/256))
			self.Create_zones()
			self.Create_Line()

	def on_Advanced_Button_Clicked(self,widget):
		if self.Advanced_Mode:
			self.AlienFX_Main_Windows
			widget.set_label("Show Advanced")
			self.AlienFX_Configurator_ScrollWindow.hide()
			self.AlienFX_Inside_vBox.children()[2].hide()
			self.AlienFX_Inside_vBox.children()[2].set_size_request(-1,0)
			#self.AlienFX_Configurator_ScrollWindow.hide()
			self.AlienFX_Inside_vBox.children()[1].show()
			#self.AlienFX_Inside_vBox.children()[2].set_size_request(-1,0)
			self.Advanced_Mode = False
			self.Create_zones()
			#self.AlienFX_Main_Windows.realize()
			self.AlienFX_Main_Windows.resize(800, 200)
		else:
			self.Advanced_Mode = True
			self.Create_Line()
			self.AlienFX_Configurator_ScrollWindow.show()
			self.AlienFX_Inside_vBox.children()[2].show()
			self.AlienFX_Inside_vBox.children()[2].set_size_request(-1,350)
			self.AlienFX_Inside_vBox.children()[1].hide()
			widget.set_label("Hide Advanced")
			#self.AlienFX_Main_Windows.realize()
			self.AlienFX_Main_Windows.resize(800, 600)

	def on_AlienFX_Tempo_Changed(self,widget,scroll,value):
		self.speed = int(value*256)
		self.configuration.speed = self.speed
		#print self.speed

	
	def on_AlienFX_ColorSelection_Dialog_Ok(self,widget):
		colorsel = self.AlienFX_ColorSelection_Window.colorsel
		color = colorsel.get_current_color()
		r = color.red/256
		g = color.green/256
		b = color.blue/256
		if r == 0:
			r = "00"
		else:
			r = hex(r).replace('0x','')
		if g == 0:
			g = "00"
		else:
			g = hex(g).replace('0x','')
		if b == 0:
			b = "00"
		else:
			b = hex(b).replace('0x','')
		
		color = "%s%s%s"%(r,g,b)
		self.AlienFX_ColorSelection_Window.hide()
		self.on_AlienFX_Color_Panel_Clicked(self,self,color)

	def on_AlienFX_ColorSelection_Dialog_Cancel(self,widget):
		self.AlienFX_ColorSelection_Window.hide()
	
	def on_color_select_button_Clicked(self,widget):
		self.AlienFX_ColorSelection_Window.show()
	
	def on_Apply_pressed(self,widget):
		self.Set_Conf()
	
	def on_Save_pressed(self,widget):
		self.Set_Conf(Save=True)
	
	def on_Line_AddConf_pressed(self,widget, zone, conf):
		self.configuration.area[zone.name].append("fixed", self.default_color, self.default_color)
		#print zone.line
		self.Create_zones()
		self.Create_Line()
	
	def on_AlienFX_Color_Panel_Clicked(self,widget, event, color):
		if self.set_color == 1:
			self.selected_color1 = color
			self.configuration.area[self.selected_area.name].update_line(self.selected_Id,color1 = self.selected_color1)
		else:
			self.selected_color2 = color
			self.configuration.area[self.selected_area.name].update_line(self.selected_Id,color2 = self.selected_color2)
		if self.selected_area and self.selected_mode and self.selected_color1 and self.auto_apply and self.selected_Id == 1:
			if self.selected_mode == "morph" and self.selected_color2 and not self.selected_area.power_button:
				self.Set_color()
			elif self.selected_mode != "morph" and not self.selected_area.power_button:
				self.Set_color()
		#print self.configuration.area[self.selected_area.name].line[self.selected_Id]
		self.Create_zones()
		self.Create_Line()
	
	def on_AlienFX_Preview_Zone_Clicked(self,widget,event,zone,Id,color):
		self.selected_area = zone
		self.selected_Id = Id
		self.selected_mode = self.configuration.area[zone.name][self.selected_Id].mode
		self.selected_color1 = self.configuration.area[zone.name][self.selected_Id].color1
		self.selected_color2 = self.configuration.area[zone.name][self.selected_Id].color2
		if self.selected_mode == "morph" or zone.power_button:
			self.set_color = color
		else:
			self.set_color = 1
		#print "Hey ! Color %s clicked ! Area : %s"%(color,zone.description)
		
	def on_AlienFX_Preview_Mode_Clicked(self, widget, event, mode, zone, confId):
		self.selected_mode = mode
		self.selected_Id = confId
		#self.computer.regions[zone.name].mode = mode
		self.selected_area = zone
		if self.selected_area and self.selected_mode and self.selected_color1 and self.auto_apply and self.selected_Id == 1:
			if self.selected_mode == "morph" and self.selected_color2:
				self.Set_color()
			elif self.selected_mode != "morph":
				self.Set_color()
		self.configuration.area[self.selected_area.name].update_line(self.selected_Id,mode = self.selected_mode)
		self.Create_zones()
		self.Create_Line()

	def on_AlienFX_Menu_AutoApply(self,widget):
		if self.auto_apply:
			self.auto_apply = False
		else:
			self.auto_apply = True
		
	def on_AlienFX_Main_Window_destroy(self,widget):
		gtk.main_quit()
		
		
	def on_Configuration_New(self,widget):
		if os.path.isfile(self.actual_conf_file):
			if not self.configuration.Check(self.actual_conf_file):
				messagedialog = gtk.Dialog("The configuration has changed ! Do you want to save it before creating a new one?", None, gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_NO, gtk.RESPONSE_NO, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
				response = messagedialog.run()
				if response == gtk.RESPONSE_OK:
					self.configuration.Save(self.actual_conf_file)
				elif response == gtk.RESPONSE_NO:
					print 'Conf Not saved !'
				messagedialog.destroy()
		self.on_New_Conf()
		self.Create_zones()
		self.Create_Line()

	def on_Configuration_Open(self,widget):
		chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_OPEN,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		filter = gtk.FileFilter()
		filter.set_name("Conf Files")
		filter.add_pattern("*.cfg")
		chooser.add_filter(filter)
		chooser.set_current_folder('.')
		response = chooser.run()
		if response == gtk.RESPONSE_OK:
			self.actual_conf_file = chooser.get_filename()
			self.configuration = AlienFXConfiguration()
			self.configuration.Load(self.actual_conf_file)
		elif response == gtk.RESPONSE_CANCEL:
			print 'Closed, no files selected'
		chooser.destroy()
		self.Create_zones()
		self.Create_Line()
		
	def on_Configuration_Save(self,widget):
		self.configuration.Save(self.actual_conf_file)

	def on_Configuration_Save_As(self,widget):
		chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_SAVE,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
		filter = gtk.FileFilter()
		filter.set_name("Conf Files")
		filter.add_pattern("*.cfg")
		chooser.add_filter(filter)
		chooser.set_current_folder('.')
		response = chooser.run()
		if response == gtk.RESPONSE_OK:
			self.actual_conf_file = chooser.get_filename()
			self.configuration.Save(self.actual_conf_file)
		elif response == gtk.RESPONSE_CANCEL:
			print 'Closed, no files selected'
		chooser.destroy()
		self.Create_zones()
		self.Create_Line()
	
	def on_Remove_Clicked(self,widget,bla,zone,conf):
		if len(self.configuration.area[zone.name]) > 1:
			self.configuration.area[zone.name].remove(conf)
		self.Create_zones()
		self.Create_Line()
		
	def on_color_focus_in(self,widget,event,zone,conf):
		if not zone.power_button:
			if conf > 0:
				try :
					if self.remove_box:
						self.remove_box.destroy()
				except:
					pass
				#self.Remove_button_destroy = False
				self.remove_box = gtk.Fixed()
				self.remove_button = gtk.Button()
				self.remove_button.set_label("X")
				self.remove_button.connect("clicked",self.on_Remove_Clicked, zone,conf)
				#self.remove_button.connect("destroy-event",self.on_Remove_button_destroy)
				#self.remove_button.connect("enter-notify-event",self.on_Remove_button_focus_in)
				#self.remove_button.connect("leave-notify-event",self.on_Remove_button_focus_out)
				self.remove_button.set_size_request(20,20)
				self.remove_box.put(self.remove_button,40,0)
				#widget.set_above_child(False)
				#print widget.get_parent()
				widget.add(self.remove_box)
				#print "ABOVE ?",widget.get_above_child()
				self.remove_box.show_all()
				#print "Focus IN :x = %s y = %s    %s, %s, %s"%(event.x,event.y,zone.description,conf,widget.get_size_request())
	
	def on_color_focus_out(self,widget,event,zone,conf):
		#print widget
		#if not self.Remove_button_destroy:
			#self.remove_box.destroy()
		try:
			if event.x > 40 and event.x < 60 and event.y < 20 and event.y > 1:
				pass
			else:
				self.remove_box.destroy()
		except:
			pass
		#print "Focus OUT : x = %s y = %s %s, %s"%(event.x,event.y,zone.description,conf)

	def __textbackground(self,widget,ev,image):
		widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL],image, 0, 0, 0, 0)
		if widget.get_child() != None:
			widget.propagate_expose(widget.get_child(), ev)
		return True
		
	def on_AlienFX_Menu_Light_Off(self,widget):
		#print "OFF"
		if self.lights:
			self.controller.Reset(self.computer.RESET_ALL_LIGHTS_OFF)
			try:
        self.controller.Send_Packet()
      except:
        pass
		self.lights = False
		
	def on_AlienFX_Menu_Light_On(self,widget):
		#print "ON"
		if not self.lights:
			self.Set_Conf()
		self.lights = True
	
	def Not_Yet(self,widget):
		messagedialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, "This feature is not yet available !")
		messagedialog.run()
		messagedialog.destroy()

	def on_AlienFX_ColorSelection_Windows_Close(self,widget):
		pass

	def on_AlienFX_ColorSelection_Windows_Destroy(self,widget):
		pass
		
		
class Image_DB:
	def __init__(self):
		self.AlienFX_Main_Eventbox = './images/AlienFX_Main_Eventbox.jpg'
		self.AlienFX_Icon_Fixed_On = './images/fixed_on.png'
		self.AlienFX_Icon_Fixed_Off = './images/fixed_off.png'
		self.AlienFX_Icon_Blink_On = './images/blink_on.png'
		self.AlienFX_Icon_Blink_Off = './images/blink_off.png'
		self.AlienFX_Icon_Morph_On = './images/morph_on.png'
		self.AlienFX_Icon_Morph_Off = './images/morph_off.png'
		self.AlienFX_Cadre_01_Up_Left = './images/carde_up_left.png'
		self.AlienFX_Cadre_01_Up_Middle = './images/carde_up_middle.png'
		self.AlienFX_Cadre_01_Up_Right = './images/carde_up_right.png'
		self.AlienFX_Cadre_01_Up_Right_c = './images/carde_up_right_c.png'
		self.AlienFX_Cadre_01_Left = './images/carde_left.png'
		self.AlienFX_Cadre_01_Right = './images/carde_right.png'
		self.AlienFX_Cadre_01_Bottom_Left = './images/carde_bottom_left.png'
		self.AlienFX_Cadre_01_Bottom_Middle = './images/carde_bottom_middle.png'
		self.AlienFX_Cadre_01_Bottom_Right = './images/carde_bottom_right.png'
		self.AlienFX_Cadre_02_Up_Left = './images/cadre1_up_left.png'
		self.AlienFX_Cadre_02_Up_Middle = './images/cadre1_up_middle.png'
		self.AlienFX_Cadre_02_Up_Right = './images/cadre1_up_right.png'
		self.AlienFX_Cadre_02_Left = './images/cadre1_left.png'
		self.AlienFX_Cadre_02_Right = './images/cadre1_right.png'
		self.AlienFX_Cadre_02_Bottom_Left = './images/cadre1_bottom_left.png'
		self.AlienFX_Cadre_02_Bottom_Middle = './images/cadre1_bottom_middle.png'
		self.AlienFX_Cadre_02_Bottom_Right = './images/cadre1_bottom_right.png'
		self.AlienFX_Cadre_0_Up_Left = './images/carde0_up_left.png'
		self.AlienFX_Cadre_0_Up_Left2 = './images/carde0_up_left2.png'
		self.AlienFX_Cadre_0_Up_Middle = './images/carde0_up_middle.png'
		self.AlienFX_Cadre_0_Up_Right = './images/carde0_up_right.png'
		self.AlienFX_Cadre_0_Up_Right2 = './images/carde0_up_right2.png'
		self.AlienFX_Cadre_0_Left = './images/carde0_left.png'
		self.AlienFX_Cadre_0_Right = './images/carde0_right.png'
		self.AlienFX_Cadre_0_Bottom_Left = './images/carde0_bottom_left.png'
		self.AlienFX_Cadre_0_Bottom_Middle_Left = './images/carde0_bottom_middle_l.png'
		self.AlienFX_Cadre_0_Bottom_Middle = './images/carde0_bottom_middle_m.png'
		self.AlienFX_Cadre_0_Bottom_Middle_Right = './images/carde0_bottom_middle_r.png'
		self.AlienFX_Cadre_0_Bottom_Right = './images/carde0_bottom_right.png'


class Daemon_Controller:
	def __init__(self):
		self.HOST = 'localhost'
		self.PORT = 25436
		self.ADDR = (self.HOST,self.PORT)
		self.sock = None
		self.BUFSIZE = 4096
		self.request = []

	def makeConnection(self):
		self.sock = socket(AF_INET, SOCK_STREAM)
		try:
			self.sock.connect(self.ADDR)
			self.sock.settimeout(1)
			return True
		except error,e:
			if "[Errno 111]" in str(e):
				print "the Deamon is disconnected ... "
			else:
				print e
			print "Trying to load the driver manually"
			return False

	def sendCmd(self, cmd):
		self.sock.send(cmd)

	def getResults(self):
		data = self.sock.recv(self.BUFSIZE)
		return data

	def Set_Loop(self,action):
		packet = ["Set_Loop",str(action)]
		self.request.append(packet)

	def Set_Loop_Conf(self,Save=False,block = 0x01):
		packet = ["Set_Loop_Conf",str(Save),str(block)]
		self.request.append(packet)

	def Add_Loop_Conf(self,area,mode,color1,color2=None):
		packet = ["Add_Loop_Conf",str(hex(area)).replace('0x',''),str(mode),str(color1),str(color2)]
		self.request.append(packet)

	def Add_Speed_Conf(self,speed = 0xc800):
		packet = ["Add_Speed_Conf",str(speed)]
		self.request.append(packet)
		
	def End_Loop_Conf(self):
		packet = ["End_Loop_Conf",""]
		self.request.append(packet)

	def End_Transfert_Conf(self):
		packet = ["End_Transfert_Conf",""]
		self.request.append(packet)

	def Write_Conf(self):
		packet = ["Write_Conf",""]
		self.request.append(packet)
		self.Send_Packet()

	def Set_Color(self, Area, Color, Save = False, Apply = False, block = 0x01):
		packet = ["Set_Color",str(hex(Area)).replace('0x',''),str(Color),str(Save),str(Apply),str(block)]
		self.request.append(packet)
		self.Send_Packet()

	def Set_Color_Blink(self,Area,Color, Save = False, Apply = False, block = 0x01):
		packet = ["Set_Color_Blink",str(hex(Area)).replace('0x',''),str(Color),str(Save),str(Apply),str(block)]
		self.request.append(packet)
		self.Send_Packet()

	def Set_Color_Morph(self,Area,Color1,Color2, Save = False, Apply = False, block = 0x01):
		packet = ["Set_Color_Morph",str(hex(Area)).replace('0x',''),str(Color1),str(Color2),str(Save),str(Apply),str(block)]
		self.request.append(packet)
		self.Send_Packet()

	def WaitForOk(self):
		packet = ["WaitForOk",""]
		self.request.append(packet)

	def Get_State(self):
		packet = ["Get_State",""]
		self.request.append(packet)

	def Reset(self,res_cmd):
		packet = ["Reset",str(res_cmd)]
		self.request.append(packet)

	def Send_Packet(self):
		tmp = []
		for el in self.request:
			tmp.append(",".join(el))
		cmd = "|".join(tmp)
		self.sendCmd(cmd)
		self.RAZ()
		resp = self.getResults()
		print resp
		if resp != "executed":
			raise ValueError("Error while communicating with the daemon !")

	def Ping(self):
		print "Sending Ping"
		self.sendCmd("PING")
		print "Sent ..."
		pong = self.getResults()
		print "Server Answer : ",pong
		if pong != "PONG":
			return False
		return True
	
	def RAZ(self):
		self.request = []

	def Bye(self):
		self.sendCmd("BYE")

if __name__ == "__main__":
	gui = pyAlienFX_GUI()
	gui.main()
	gui.controller.Bye()
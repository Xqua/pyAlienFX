
from AlienFX.AlienFXTexts import *
from AlienFXComputers import *


class AlienFXConfiguration:
	def __init__(self):
		self.name = "Default configuration"
		self.area = {}
		self.computer = ""
		self.AlienFXTexts = AlienFXTexts()
	
	def Create(self,name,computer,speed,path):
		self.name = name
		self.computer = computer
		self.speed = speed
		self.path = path
		
	def Add(self,area):
		if not self.area.has_key(area.name):
			self.area[area.name] = configuration(area)
		#else:
			#self.area[area.name].append(configuration(area))
	
	def Show_Configuration(self):
		print "\t%s\n=== === === === === ===\n"%self.name
		print "Speed %s\n"%self.speed
		for area in self.area:
			print "      %s\n      =============      \n"%self.area[area].description
			for element in self.area[area]:
				print element.text

	def Show_Area(self,area):
		print "      %s\n      =============      \n"%self.area[area].description
		if self.area.has_key(area):
			for element in self.area[area]:
				print element.text
	
	def Save(self,path=None):
		if path:
			self.path = path
		f = open(self.path,'w')
		f.write("name=%s\n"%self.name)
		f.write("computer=%s\n"%self.computer)
		f.write("speed=%s\n"%self.speed)
		for area in self.area.keys():
			f.write("area=%s\n"%area)
			for element in self.area[area]:
				f.write("type=%s\n"%element.mode)
				f.write("color=%s\n"%element.color1)
				f.write("color2=%s\n"%element.color2)
		f.close()
	
	def Load(self,path):
		if path:
			self.path = path
		f = open(path)
		lines = f.readlines()
		for line in lines:
			split = line.strip().split('=')
			
			if split[0] == "name":
				self.name = split[1]
			elif split[0] == "speed":
				self.speed = int(split[1])
			elif split[0] == "computer":
				self.computer = split[1]
			elif split[0] == "area":
				area = split[1]
				self.area[split[1]] = configuration(AllComputers.computerList[self.computer].computer.regions[area])
			elif split[0] == "type":
				self.area[area].append(split[1])
			elif split[0] == "color":
				self.area[area][-1].color1 = split[1]
			elif split[0] == "color2":
				self.area[area][-1].color2 = split[1]
				
	def Check(self,path):
		old = AlienFXConfiguration()
		old.Load(path)
		if self.name != old.name:
			print "name"
			return False
		if self.speed != old.speed:
			print "speed"
			return False
		if self.computer != old.computer:
			print "computer"
			return False
		#print "self.area: ",self.area
		#print "old.area : ",old.area
		for area in self.area:
			if area not in old.area.keys():
				print "AREA ERROR"
				return False
			for i in range(len(self.area[area])):
				try:
					if self.area[area][i].mode != old.area[area][i].mode:
						return False
					if self.area[area][i].color1 != old.area[area][i].color1:
						return False
					if self.area[area][i].color2 != old.area[area][i].color2:
						return False
				except:
					return False
		#if self.area != old.area:
			#return False
		return True
		
		
class configuration(list,AlienFXTexts):
	def __init__(self,area):
		self.area = area.name
		self.description = area.description
		self.Id = 0x01

		
	def append(self,Type, color = "", color2 = ""):
		el = element(Type,color,color2)
		el.Id = self.Id
		self += [el]
		self.Id += 1

	def update_line(self,Id,mode=None,color1=None,color2=None):
		if len(self) > Id:
			if mode:
				self[Id].mode = mode
			if color1:
				self[Id].color1 = color1
			if color2:
				self[Id].color2 = color2
			return True
		return False
	
	def remove(self,Id):
		for i in range(Id,len(self)-1):
			self[i].Id -= 1 
		del self[Id]
		
class element():
	def __init__(self, Type, color = "", color2 = ""):
		self.mode = Type
		self.Id = 0x00
		self.color1 = color
		self.color2 = color2
		self.Text_Conf_Type = {
		"fixed" : "Setting fixed color to %s%s",
		"blink" : "Setting blinking color to %s%s",
		"morph" : "Setting morph color from %s to %s",
		"speed" : "Setting Speed to %s%s",
		"endloop" : "End of the loop%s%s"}
		#print "-%s-"%self.mode
		self.text = self.Text_Conf_Type[self.mode]%(self.color1,self.color2)
	
	
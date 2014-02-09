#!/usr/bin/python

import sys

class parser:
	def __init__(self,path):
		f = open(path)
		self.string = f.readlines()
		self.clean()
		self.Strip()
		self.Print()
	
	def clean(self):
		tmp = []
		for l in xrange(len(self.string)):
			if "    " in self.string[l]:
				tmp.append(self.string[l])
		self.string = tmp
		
	def Strip(self):
		for l in range(len(self.string)):
			self.string[l] = self.string[l].strip()
		for l in range(len(self.string)):
			tmp = ""
			for i in self.string[l]:
				if i != " ":
					tmp += i
			self.string[l] = tmp
		tmp = []
		for l in self.string:
			try:
				int(l,16)
				tmp.append(l)
			except:
				pass
		self.string = tmp
	
	def Print(self):
		for l in range(len(self.string)):
			n = 0
			tmp = ""
			for i in self.string[l]:
				if n == 1:
					n = 0
					tmp += "%s "%i
				else:
					tmp += i
					n += 1
			self.string[l] = tmp
			
		for l in self.string:
			print l

if __name__ == "__main__":
	if len(sys.argv) == 2:
		pa = parser(sys.argv[1])
	else:
		print "Usage : usbmonparser.py [File]"
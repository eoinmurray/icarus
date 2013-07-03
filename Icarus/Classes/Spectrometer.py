import numpy as np 

class Spectrometer:
	def __init__(self):
		self.x = 0
		self.xx = 0

	def hit(self, name):
		if name == 'XX':
			self.xx += 1
		if name == 'X' :
			self.x += 1

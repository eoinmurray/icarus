import numpy as np 

class Laser:
	def __init__(self, pulse_width=None, power=None):
		self.pulse_width = pulse_width
		self.power = power

	def pulseTimes(self, maxTime):
		return np.floor(np.linspace(0,maxTime, num=(maxTime+self.pulse_width)/(self.pulse_width)))
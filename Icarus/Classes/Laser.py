


import numpy as np 



class Laser:
	"""
		Laser or pump class, has only power and pulses
	"""



	def __init__(self, pulse_width=None, power=None):
		"""
			Init passed params.
		"""

		self.pulse_width = pulse_width
		self.power = power



	def pulseTimes(self, maxTime):
		"""
			Returns pulse times up to maxTime.
		"""

		return np.floor(np.linspace(0,maxTime, num=(maxTime+self.pulse_width)/(self.pulse_width)))
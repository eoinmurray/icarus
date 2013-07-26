


import numpy as np 



class Spectrometer:
	"""
		Records emission hits for power dependance.
	"""


	def __init__(self):
		"""
			Initialize.
		"""

		self.x = 0
		self.xx = 0




	def hit(self, name):
		"""
			Registers a hit.
		"""

		if name == 'XX':
			self.xx += 1
		if name == 'X' :
			self.x += 1

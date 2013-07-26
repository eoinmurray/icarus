


import numpy as np
from utils.EventEmitter import EventEmitter



class Detector(EventEmitter):
	"""
		The class for a detector, which will normally be added to a channel.
	"""



	def __init__(self, delay=None, efficiency=None, sigma=None, matrix=None):
		"""
			Init all the things.
		"""
		
		self.efficiency = efficiency
		self.sigma 		= sigma
		self.delay 		= delay
		self.matrix		= matrix
		self.time_tags 	= np.array([])



	def hit(self, t, lifetime):
		"""
			Check if the efficiency can take the hit, if so register it.
		"""
		
		if np.random.random_sample() < self.efficiency:
			self.register_hit(t, lifetime)



	def register_hit(self, t, lifetime):
		"""
			Adds a hit to the time tags, according to the jitter in the detectors.
			Emits and event that the parent channel will pick up.
		"""
		
		if self.sigma > 0:
			norm 	= np.random.normal(0, self.sigma, 1)[0]
		else:
			norm = 0
		time  	= t + lifetime + self.delay + norm
		self.time_tags  = np.append(self.time_tags,   [time])
		self.trigger('change')



	def reset(self):
		"""
			Resets the tags.
		"""
		
		self.time_tags = np.array([])



	def times(self):
		"""
			Returns the tags.
		"""
		
		return self.time_tags

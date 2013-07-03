import numpy as np
from utils.EventEmitter import EventEmitter

class Detector(EventEmitter):
	def __init__(self, delay=None, efficiency=None, sigma=None, matrix=None):
		self.efficiency = efficiency
		self.sigma 		= sigma
		self.delay 		= delay
		self.matrix		= matrix
		self.time_tags 	= np.array([])

	def hit(self, t, lifetime):
		if np.random.random_sample() < self.efficiency:
			self.register_hit(t, lifetime)

	def register_hit(self, t, lifetime):
		if self.sigma > 0:
			norm 	= np.random.normal(0, self.sigma, 1)[0]
		else:
			norm = 0
		time  	= t + lifetime + self.delay + norm
		self.time_tags  = np.append(self.time_tags,   [time])
		self.trigger('change')

	def reset(self):
		self.time_tags = np.array([])

	def times(self):
		return self.time_tags
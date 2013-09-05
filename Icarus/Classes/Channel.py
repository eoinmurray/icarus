


import numpy as np
import matplotlib.pyplot as plt 
from utils.EventEmitter import EventEmitter



class Channel(EventEmitter):
	"""
		Photon counting modules channel.
	"""



	def __init__(self, bin_width, detector1, detector2, name, mode = 'non_HBT'):
		"""
			Initializes bins, time tags and calculates the channels matrix (for entangled photon
			measurements only).
		"""

		self.bin_width = bin_width
		self.detector1 = detector1
		self.detector2 = detector2
		self._starts = np.array([])
		self._stops = np.array([])

		self.start = None 
		self.stop = None 

		self.matrix = np.kron(detector2.matrix, detector1.matrix)
		self.name = name
		
		self.initializeBins()
		self.initializeDetectorEvents()
		self.g2 = 0
		self.sidepeaks_avg = 0



	def resetTimeTags(self):
		"""
			Resets the starts and stops
		"""

		self._stops   = np.array([])
		self._starts  = np.array([])



	def getStarts(self):
		"""
			Returns the start tags.
		"""
		
		return self._starts



	def getStops(self):
		"""
			Returns the start tags.
		"""

		return self._stops	



	def get_g2(self):
		"""
			Returns g2.
		"""
		
		return self.g2



	def get_sidepeaks_avg(self):
		"""
			Returns sidepeaks_avg.
		"""
		
		return self.sidepeaks_avg



	def initializeBins(self):
		"""
			Calculates the bins.
		"""
		
		self.bins = np.linspace(0.04,400, num=400/(self.bin_width*27./1000.))
		self.counts = np.zeros(self.bins.size-1)
		self.previous_counts = np.zeros(self.bins.size-1)
		self.bin_edges = np.histogram(np.array([0]), self.bins)[1][0:self.bins.size-1]



	def initializeDetectorEvents(self):
		"""
			Sets up the detection hit events.
		"""
		
		def setStarts(detector):
			if self.start is None:
				self.start = detector.last_time

			self._starts = detector.time_tags
			self.real_time_process()
		
		def setStops(detector):
			if self.stop is None:
				self.stop = detector.last_time

			self._stops = detector.time_tags
			self.real_time_process()

		self.detector1.on('change', setStarts)
		self.detector2.on('change', setStops)



	def calculate_probability(self, state):
		"""
			Calculates the probability of a state hitting this channel.
		"""
		
		probability = ((np.abs( np.transpose(self.matrix)*state )**2)*4)[0,0]
		return probability



	def real_time_process(self):
		"""
			HBT needs to be processed in real time.
		"""

		if self.mode is 'HBT':
			if self.start is not None and self.stop is not None:
				temp_counts, self.bin_edges = np.histogram(self.stop - self.start, self.bins)
				self.counts += temp_counts
				self.start = None
				self.stop = None



	def processTimeTags(self):
		"""
			If both the start and stop arrays have non-zero length, then it bins the counts.
		"""
		
		if self.mode is not 'HBT':
			if (self._starts.size > 0) and (self._stops.size > 0):
				self.counts += self.processTimeTagsAlgorithm(self.bins, self._starts, self._stops)
				self.trigger('change')



	def processTimeTagsAlgorithm(self, bins, _starts, _stops):
		"""
			Calculates the corrolation between the starts and stops.
		"""
		
		counts = np.zeros(bins.size - 1)

		for stop in _stops:
			diff = stop - _starts
			diff = diff[(diff > bins.min()) & (diff < bins.max())]
			counts = counts + np.histogram(diff, bins)[0]
		return counts



	def normalize(self, pulse_width):
		"""
			Integrates the counts in each peak, and normalizes by the average of the counts in 
			the sidepeaks.
		"""
		
		hold_int = []
		hold_max = []

		x = self.bin_edges
		y = self.counts

		for j in xrange(int(x.max()/pulse_width)):
			minIdx = np.abs(x - pulse_width*j).argmin()
			maxIdx = np.abs(x - pulse_width*(j+1)).argmin()
			peakX = x[minIdx: maxIdx]
			peakY = y[minIdx:maxIdx]	
			
			if j != 6:
				hold_max.append( np.max(peakY) )
				hold_int.append( np.sum(peakY) )
			else:
				delay_peak = np.sum(peakY)

		y = y/np.mean(hold_max)

		self.previous_counts = self.counts
		self.counts = y
		self.g2 = self.calculate_g2(delay_peak, hold_int)



	def unnormalize(self):
		"""
			Return the unnormalized counts.
		"""
		
		if not self.previous_counts.all():
			self.counts = self.previous_counts



	def plotPeaks(self, pulse_width):
		"""
			Plots the individual peaks to check if the processing algorithm accurately 
			selects the peaks
		"""
		
		x = self.bin_edges
		y = self.counts
		for j in xrange(int(x.max()/pulse_width)):
			minIdx = np.abs(x - pulse_width*j).argmin()
			maxIdx = np.abs(x - pulse_width*(j+1)).argmin()
			peakX = x[minIdx: maxIdx]
			peakY = y[minIdx:maxIdx]	
			plt.plot(peakX, peakY)
		plt.show()



	def calculate_g2(self, delay_peak, hold_int):
		"""
			Divide the delay peak by the average of the sidepeaks.			
		"""
		
		if np.array(hold_int).mean() > 0:
			g2 = delay_peak/np.array(hold_int).mean()
			g2 = np.around(g2, decimals=3)
			return g2
		else:
			return 0

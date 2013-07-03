import numpy as np
import matplotlib.pyplot as plt 
from utils.EventEmitter import EventEmitter

try:
	import utils._histogram as _histogram
except ImportError:
	_histogram = np.histogram


class Channel(EventEmitter):
	def __init__(self, bin_width, detector1, detector2, name):
		self.bin_width = bin_width
		self.detector1 = detector1
		self.detector2 = detector2
		self._starts = np.array([])
		self._stops = np.array([])
		self.matrix = np.kron(detector2.matrix, detector1.matrix)
		self.name = name
		
		self.initializeBins()
		self.initializeDetectorEvents()
		self.g2 = 0
		self.sidepeaks_avg = 0

	def resetTimeTags(self):
		self._stops   = np.array([])
		self._starts  = np.array([])

	def getStarts(self):
		return self._starts

	def getStops(self):
		return self._stops	

	def get_g2(self):
		return self.g2

	def get_sidepeaks_avg(self):
		return self.sidepeaks_avg

	def initializeBins(self):
		self.bins = np.linspace(0.04,400, num=400/(self.bin_width*27./1000.))
		self.counts = np.zeros(self.bins.size-1)
		self.previous_counts = np.zeros(self.bins.size-1)
		self.bin_edges = np.histogram(np.array([0]), self.bins)[1][0:self.bins.size-1]

	def initializeDetectorEvents(self):
		def setStarts(detector):
			self._starts = detector.time_tags
		
		def setStops(detector):
			self._stops = detector.time_tags

		self.detector1.on('change', setStarts)
		self.detector2.on('change', setStops)


	def calculate_probability(self, state):
		probability = ((np.abs( np.transpose(self.matrix)*state )**2)*4)[0,0]
		return probability

	def processTimeTags(self):
		if (self._starts.size > 0) and (self._stops.size > 0):
			self.counts += self.processTimeTagsAlgorithm(self.bins, self._starts, self._stops)
			self.trigger('change')

	def processTimeTagsAlgorithm(self, bins, _starts, _stops):
		counts = np.zeros(bins.size - 1)

		for stop in _stops:
			diff = stop - _starts
			diff = diff[(diff > bins.min()) & (diff < bins.max())]
			counts = counts + _histogram(diff, bins)[0]
		return counts

	def normalize(self, pulse_width):
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
		if not self.previous_counts.all():
			self.counts = self.previous_counts

	def plotPeaks(self, pulse_width):
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
		if np.array(hold_int).mean() > 0:
			g2 = delay_peak/np.array(hold_int).mean()
			g2 = np.around(g2, decimals=3)
			return g2
		else:
			return 0

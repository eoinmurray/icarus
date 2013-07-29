


import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) ; sys.path.insert(0,parentdir)
from Classes.utils.EventEmitter import EventEmitter
import numpy as np
import Icarus as icarus



class Experiment(EventEmitter):
	"""
		The main experiment class, most experiment designs will only interact with this class.
	"""



	def __init__(self, constants, Visualizer= None):
		"""
			Imports all the nessecary classes from Icarus and sets them up.
		"""


		self.constants = constants

		self.qd = icarus.QuantumDot( 
			xlifetime  = self.constants.xtau, 
			xxlifetime = self.constants.xxtau, 
			ptau = self.constants.ptau, 
			FSS = self.constants.FSS,
			crosstau = self.constants.crosstau
		)

		self.spectrometer = icarus.Spectrometer()

		self.bench = icarus.OpticalBench()
		self.bench.setQWP(0, 0)
		self.bench.setHWP(0, 0)
		
		self.laser = self.bench.Laser(
			pulse_width = self.constants.pulse_width, 
			power = self.constants.power
		)

		self.pcm = icarus.PhotonCountingModule()
		
		self.pcm.register_detector('D1',  
			self.pcm.Detector(
				delay = self.constants.delay, 	
				efficiency	= self.constants.efficiency, 
				sigma	= self.constants.sigma, 
				matrix = self.bench.jxh 
			)
		)

		self.pcm.register_detector('D2',  
			self.pcm.Detector(
				delay = self.constants.delay, 	
				efficiency	= self.constants.efficiency, 
				sigma	= self.constants.sigma, 
				matrix = self.bench.ixv 
			)
		)

		self.pcm.register_detector('D3',  
			self.pcm.Detector(
				delay = 0, 	
				efficiency	= self.constants.efficiency, 
				sigma	= self.constants.sigma, 
				matrix = self.bench.ixxh 
			)
		)
		
		self.pcm.register_detector('D4',  
			self.pcm.Detector(
				delay = 0, 	
				efficiency	= self.constants.efficiency, 
				sigma	= self.constants.sigma, 
				matrix = self.bench.jxxv 
			)
		)
		
		self.pcm.register_channel('D1D3',
			self.pcm.Channel(
				constants.bin_width, 
				self.pcm.detector('D3'), 
				self.pcm.detector('D1'), 
				'D1D3'
			)
		)
		
		self.pcm.register_channel('D1D4',
			self.pcm.Channel(
				constants.bin_width, 
				self.pcm.detector('D4'), 
				self.pcm.detector('D1'), 
				'D1D4'
			)
		)
		
		self.pcm.register_channel('D2D3',
			self.pcm.Channel(
				constants.bin_width, 
				self.pcm.detector('D3'), 
				self.pcm.detector('D2'), 
				'D2D3'
			)
		)
		
		self.pcm.register_channel('D2D4',
			self.pcm.Channel(
				constants.bin_width, 
				self.pcm.detector('D4'), 
				self.pcm.detector('D2'), 
				'D2D4'
			)
		)

		self.Visualizer = Visualizer
		if Visualizer:
			self.visualizer = icarus.Visualizer()
			self.visualizer.add(self.pcm.channel('D1D3'), 221)
			self.visualizer.add(self.pcm.channel('D1D4'), 222)
			self.visualizer.add(self.pcm.channel('D2D3'), 223)
			self.visualizer.add(self.pcm.channel('D2D4'), 224)

			self.visualizer.bind('D1D3')
			self.visualizer.bind('D1D4')
			self.visualizer.bind('D2D3')
			self.visualizer.bind('D2D4')



	def run(self, name):
		"""
			Is called by the super importing module. Runs the specified algorithm.
		"""


		for interation in xrange(self.constants.num_iterations):
			self.pcm.detector('D1').reset()
			self.pcm.detector('D2').reset()
			self.pcm.detector('D3').reset()
			self.pcm.detector('D4').reset()

			self.pcm.channel('D1D3').resetTimeTags()
			self.pcm.channel('D1D4').resetTimeTags()
			self.pcm.channel('D2D3').resetTimeTags()
			self.pcm.channel('D2D4').resetTimeTags()

			getattr(icarus.Algorithms, name)(self.qd, self.pcm, self.laser, self.bench, self.spectrometer, self.constants)

			self.pcm.channel('D1D3').processTimeTags()
			self.pcm.channel('D1D4').processTimeTags()
			self.pcm.channel('D2D3').processTimeTags()
			self.pcm.channel('D2D4').processTimeTags()

			self.trigger('tick')
		if self.Visualizer:
			self.visualizer.plt.ioff()



	def plot(self):
		"""
			Makes a static plot of each detector.
		"""

		if not self.Visualizer:
			self.visualizer = icarus.Visualizer()
		self.visualizer.plt.ioff()		
		self.visualizer.plot(self.pcm.channel('D1D3'), 221)
		self.visualizer.plot(self.pcm.channel('D1D4'), 222)
		self.visualizer.plot(self.pcm.channel('D2D3'), 223)
		self.visualizer.plot(self.pcm.channel('D2D4'), 224)



import time
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

import numpy as np
from Icarus import Icarus
import Algorithms as Algorithms

class Experiment:
	def __init__(self, constants, Visualizer= None):
		self.icarus = Icarus()

		self.constants = constants

		self.qd = self.icarus.QuantumDot( 
			xlifetime  = self.constants.xtau, 
			xxlifetime = self.constants.xxtau, 
			ptau = self.constants.ptau, 
			FSS = self.constants.FSS
		)

		self.spectrometer = self.icarus.Spectrometer()

		self.bench = self.icarus.OpticalBench()

		# These are defaults, they should generally be changed by the experiment algorithm.
		self.bench.setHWP(np.pi/8, np.pi/8)
		self.bench.setQWP(0, 0)
		self.bench.setLabMatrix('NBSNBS HWPHWP SS PBSPBS')

		self.laser = self.bench.Laser(
			pulse_width = self.constants.pulse_width, 
			power = self.constants.power
		)

		self.pcm = self.icarus.PhotonCountingModule()
		
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
			self.visualizer = self.icarus.Visualizer()
			self.visualizer.add(self.pcm.channel('D1D3'), 221)
			self.visualizer.add(self.pcm.channel('D1D4'), 222)
			self.visualizer.add(self.pcm.channel('D2D3'), 223)
			self.visualizer.add(self.pcm.channel('D2D4'), 224)

			self.visualizer.bind('D1D3')
			self.visualizer.bind('D1D4')
			self.visualizer.bind('D2D3')
			self.visualizer.bind('D2D4')

	def run(self, name):

		for interation in xrange(self.constants.num_iterations):
			self.pcm.detector('D1').reset()
			self.pcm.detector('D2').reset()
			self.pcm.detector('D3').reset()
			self.pcm.detector('D4').reset()

			self.pcm.channel('D1D3').resetTimeTags()
			self.pcm.channel('D1D4').resetTimeTags()
			self.pcm.channel('D2D3').resetTimeTags()
			self.pcm.channel('D2D4').resetTimeTags()

			getattr(Algorithms, name)(self.qd, self.pcm, self.laser, self.bench, self.spectrometer, self.constants)

			self.pcm.channel('D1D3').processTimeTags()
			self.pcm.channel('D1D4').processTimeTags()
			self.pcm.channel('D2D3').processTimeTags()
			self.pcm.channel('D2D4').processTimeTags()

			self.icarus.trigger('tick')
		if self.Visualizer:
			self.visualizer.plt.ioff()

	def plot(self):
		if not self.Visualizer:
			self.visualizer = self.icarus.Visualizer()
		self.visualizer.plt.ioff()		
		self.visualizer.plot(self.pcm.channel('D1D3'), 221)
		self.visualizer.plot(self.pcm.channel('D1D4'), 222)
		self.visualizer.plot(self.pcm.channel('D2D3'), 223)
		self.visualizer.plot(self.pcm.channel('D2D4'), 224)

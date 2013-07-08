

import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

import numpy as np 
import matplotlib.pyplot as plt
from Icarus import Icarus
from constants import Constants

def state(qd, bench, xlifetime, fss):
	"""Calculates the state at the beginning and end of the bench."""

	qd.FSS = fss
	qd.xlifetime = xlifetime
	qd.xxlifetime = xlifetime/2
	
	state = qd.generate_state()
	propogated_state = bench.matrix*state
	return propogated_state

def test():
	"""Testing D1D3 probability versus fss."""

	icarus = Icarus()
	constants = Constants()

	size = 5000
	xtau = np.random.exponential(1, 1)[0]
	FSS = np.linspace(0, 4, num=100)*1e-6
	hbar = 6.56e-16

	qd = icarus.QuantumDot(xtau, xtau/2, FSS)
	
	bench = icarus.OpticalBench()
	bench.setHWP(np.pi/8, np.pi/8)
	bench.setLabMatrix('NBSNBS HWPHWP SS PBSPBS')
		
	pcm = icarus.PhotonCountingModule()
	pcm.register_detector('D1',  
		pcm.Detector(
			delay = constants.delay, 	
			efficiency	= constants.efficiency, 
			sigma	= constants.sigma, 
			matrix = bench.jxh 
		)
	)
	pcm.register_detector('D3',  
		pcm.Detector(
			delay = 0, 	
			efficiency	= constants.efficiency, 
			sigma	= constants.sigma, 
			matrix = bench.ixxh 
		)
	)

	pcm.register_detector('D2',  
		pcm.Detector(
			delay = constants.delay, 	
			efficiency	= constants.efficiency, 
			sigma	= constants.sigma, 
			matrix = bench.ixv 
		)
	)
	
	pcm.register_channel('D1D3', 
		pcm.Channel(
			constants.bin_width, 
			pcm.detector('D3'), 
			pcm.detector('D1'), 
			'D1D3'
		)
	)

	pcm.register_channel('D2D3', 
		pcm.Channel(
			constants.bin_width, 
			pcm.detector('D3'), 
			pcm.detector('D2'), 
			'D2D3'
		)
	)

	channel1 = pcm.channel('D1D3')
	channel2 = pcm.channel('D2D3')
	
	states = [state(qd, bench, xtau, f) for f in FSS]
	D1D3_probs = np.array([channel1.calculate_probability(i) for i in states])
	D2D3_probs = np.array([channel2.calculate_probability(i) for i in states])
	
	plt.plot(FSS/1e-6, D1D3_probs, 'go')
	plt.plot(FSS/1e-6, D2D3_probs, 'bo')
	plt.show()

if __name__ == "__main__":
	test()
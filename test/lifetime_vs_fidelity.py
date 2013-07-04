

import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

import numpy as np 
import matplotlib.pyplot as plt
from Icarus import Icarus
import constants as Constants

def state(qd, bench, xlifetime):

	qd.xlifetime = xlifetime
	qd.xxlifetime = xlifetime/2
	state = qd.generate_state()
	propogated_state = bench.matrix*state

	return propogated_state

def test():
	icarus = Icarus()
	constants = Constants.Constants()

	size = 5000
	xtau = 1.
	FSS = 0.3e-6
	hbar = 6.56e-16
	lifetimes = np.random.exponential(xtau, size=size)
	HWPAngles = np.array([0, np.pi/8, None])
	QWPAngles = np.array([None, None, np.pi/4])
	angles = np.vstack((HWPAngles, QWPAngles)).T
	
	qd = icarus.QuantumDot(xtau, xtau/2, FSS)
	bench = icarus.OpticalBench()
	degree_of_cor = []
	
	for i in angles:

		HWPAngle = i[0]
		QWPAngle = i[1]

		if HWPAngle is not None:
			bench.setHWP(HWPAngle, HWPAngle)
			bench.setLabMatrix('NBSNBS HWPHWP SS PBSPBS')
		
		elif QWPAngle is not None:
			bench.setQWP(QWPAngle, QWPAngle)
			bench.setLabMatrix('NBSNBS QWPQWP SS PBSPBS')

		pcm = icarus.PhotonCountingModule()
		pcm.register_detector('D1',  pcm.Detector(delay = constants.delay, 	efficiency	= constants.efficiency, sigma	= constants.sigma, matrix = bench.jxh ))
		pcm.register_detector('D3',  pcm.Detector(delay = 0, 	efficiency	= constants.efficiency, sigma	= constants.sigma, matrix = bench.ixxh ))
		pcm.register_detector('D4',  pcm.Detector(delay = 0, 	efficiency	= constants.efficiency, sigma	= constants.sigma, matrix = bench.jxxv ))
		
		pcm.register_channel('D1D3', pcm.Channel(constants.bin_width, pcm.detector('D3'), pcm.detector('D1'), 'D1D3'))
		pcm.register_channel('D1D4', pcm.Channel(constants.bin_width, pcm.detector('D4'), pcm.detector('D1'), 'D1D4'))

		states = [state(qd, bench, i) for i in lifetimes]
		D1D3_probs = np.array([pcm.channel('D1D3').calculate_probability(i) for i in states])
		D1D4_probs = np.array([pcm.channel('D1D4').calculate_probability(i) for i in states])

		degree_of_cor.append((D1D3_probs - D1D4_probs)/(D1D3_probs + D1D4_probs))
	
	lins  = degree_of_cor[0]
	diags = degree_of_cor[1]
	circs = degree_of_cor[2]

	fidelities = (1 + lins + diags - circs)/4
	plt.plot(lifetimes, fidelities, 'go')
	plt.show()

if __name__ == "__main__":
	test()
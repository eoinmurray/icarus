


import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
import numpy as np
import matplotlib.pyplot as plt
from constants import Constants
import Icarus.Experiment as Experiment	
import utils.save as save



def go():
	"""
		Runs auto g2 vs power.
	"""

	algoname = 'auto'
	constants = Constants()
	powers = np.linspace(0.2, 40, num=40)
	
	hold_counts = np.array([])
	hold_g2 = np.array([])
	bin_edges = np.array([])

	print 'Running g2 vs power.'

	for i in xrange(powers.size):
		print 'Iteration: ' + repr(i+1) + ' of ' + repr(powers.size) + '.', '\r\r\r\r\r\r\r',

		constants.power = powers[i]
		
		experiment = Experiment(constants, Visualizer=False)
		experiment.run(algoname)

		bin_edges = experiment.pcm.channel('D1D3').bin_edges
		counts = experiment.pcm.channel('D1D3').counts
		
		experiment.pcm.channel('D1D3').normalize(experiment.laser.pulse_width)
		g2 = experiment.pcm.channel('D1D3').g2
		if i == 0:
			hold_g2 = g2
			hold_counts = counts

		else:
			hold_counts = np.vstack((hold_counts, counts))
			hold_g2 = np.vstack((hold_g2, g2))

	powers = np.around(powers, decimals=2)
	
	plt.plot(powers, hold_g2, 'go')
	plt.ylabel('$g^{(2)}(\\tau)$')
	plt.xlabel('Mean photon number (power)')
	plt.ylim([0,hold_g2.max() + 1])
	
	save.savefig(plt, name = algoname + '-g2_v_power-secondprob' + repr(constants.secondary_emission_probability) + 'power-' + repr(experiment.laser.power))
	plt.show()



if __name__ == "__main__":
	go()


import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

import numpy as np
import matplotlib.pyplot as plt
from constants import Constants
from Experiments import Experiment

def go():
	constants = Constants()
	powers = np.linspace(0.2, 1, num=10)
	
	hold_counts = np.array([])
	hold_g2 = np.array([])
	bin_edges = np.array([])

	for i in xrange(powers.size):
		constants.power = powers[i]
		
		experiment = Experiment(constants, Visualizer=False)
		experiment.run('auto')

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

	for counts in hold_counts:
		plt.plot(bin_edges, counts)

	powers = np.around(powers, decimals=2)
	plt.legend(powers)
	plt.show()
	
	plt.plot(powers, hold_g2, 'go')
	plt.ylim([0,1])
	plt.show()

if __name__ == "__main__":
	go()
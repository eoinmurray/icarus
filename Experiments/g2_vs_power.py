import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

import numpy as np
import matplotlib.pyplot as plt
import constants as constants
from Experiments import Experiment

def smooth(array, points):
	length = np.floor(array.size/points)
	smoothed_array = np.zeros(length)
	i = 0
	while i != length:
		segment = array[i*points: (i+1)*points]
		smoothed_array[i] = np.mean(segment)

		i = i + 1
	return smoothed_array

def go():

	powers = np.concatenate((np.linspace(0.2, 4, num=15), np.linspace(4.5, 7, num=3)), axis=0)
	hold_counts = np.array([])
	hold_g2 = np.array([])
	bin_edges = np.array([])

	for i in xrange(powers.size):
		constants.power = powers[i]
		
		experiment = Experiment(constants, Visualizer=False)
		experiment.run('auto')

		experiment.pcm.channel('D1D3').normalize(experiment.laser.pulse_width)

		g2 = experiment.pcm.channel('D1D3').g2
		bin_edges = experiment.pcm.channel('D1D3').bin_edges
		counts = experiment.pcm.channel('D1D3').counts

		counts = smooth(counts, 3)

		if i == 0:
			hold_g2 = g2
			hold_counts = counts

		else:
			hold_counts = np.vstack((hold_counts, counts))
			hold_g2 = np.vstack((hold_g2, g2))

	bin_edges = smooth(bin_edges, 3)

	for counts in hold_counts:
		plt.plot(bin_edges, counts)
	plt.legend(powers)
	plt.show()

	print powers, hold_g2
	plt.plot(powers, hold_g2, 'go')
	plt.ylim([0,1])
	plt.show()

if __name__ == "__main__":
	go()
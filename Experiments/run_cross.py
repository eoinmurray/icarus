import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

from scipy import integrate, interpolate, optimize
import numpy as np
import matplotlib.pyplot as plt
from constants import Constants
from Experiment import Experiment
import utils.save as save

if __name__ == "__main__":
	constants = Constants()
	print 'Autocorrelation g2 with', constants.secondary_emission_probability, ' secondary_emission_probability.'

	experiment = Experiment(constants, Visualizer=False)
	experiment.run('cross')

	channel = experiment.pcm.channel('D1D3')
	channel.normalize(experiment.laser.pulse_width)
	
	plt.plot(channel.bin_edges - constants.delay, channel.counts)
	print 'g2:', channel.g2

	plt.ylabel('$g^{(2)}(\\tau)$')
	plt.xlabel('$\\tau(ns)$')
	plt.ylim([0, channel.counts.max() + 1])
	save.savefig(plt, name = "cross-power-" + repr(experiment.laser.power))

	plt.show()
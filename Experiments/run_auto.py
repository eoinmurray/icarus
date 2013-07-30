


import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
import numpy as np
import matplotlib.pyplot as plt
from constants import Constants
import Icarus.Experiment as Experiment	



def run_auto():
	"""
		Runs autocorrlation experiment.
	"""

	constants = Constants()
	print 'Autocorrelation g2 with', constants.secondary_emission_probability, ' secondary_emission_probability.'

	experiment = Experiment(constants, Visualizer=False)
	experiment.run('auto')

	channel = experiment.pcm.channel('D1D3')

	plt.plot(channel.bin_edges - constants.delay, channel.counts)
	channel.normalize(experiment.laser.pulse_width)
	print 'g2:', channel.g2
	
	plt.show()



if __name__ == "__main__":
	run_auto()
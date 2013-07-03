import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

from scipy import integrate, interpolate, optimize
import numpy as np
import matplotlib.pyplot as plt
import constants as constants
from Experiment import Experiment

if __name__ == "__main__":
		
	experiment = Experiment(constants, Visualizer=True)
	experiment.run('cross')
	# experiment.visualizer.plt.ioff()
	experiment.visualizer.plt.close()
	
	# plt.xlim([0, 300])
	# plt.plot(experiment.pcm.channel('D1D3').bin_edges, experiment.pcm.channel('D1D3').counts)
	# plt.show()
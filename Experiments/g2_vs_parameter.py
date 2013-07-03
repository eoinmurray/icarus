import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

from scipy import integrate, interpolate, optimize
import numpy as np
import matplotlib.pyplot as plt
import constants as constants
from Experiment import Experiment

if __name__ == "__main__":

	paramName = 'power'
	paramType = 'float'
	range_min = 0.1
	range_max = 5
	num = 15

	hold_param = np.linspace(range_min, range_max, num=num)
	hold_param = hold_param.astype(getattr(np, paramType))
	hold_g2   = []

	for param in hold_param:
		setattr(constants, paramName, param)
		
		experiment = Experiment(constants, Visualizer=False)
		experiment.run('auto')

		experiment.pcm.channel('D1D3').normalize(experiment.laser.pulse_width)

		g2 = experiment.pcm.channel('D1D3').g2
		
		hold_g2.append(g2)
		plt.close('all')

	plt.ioff()
	plt.close('all')
	plt.plot(hold_param, hold_g2, 'bo')
	plt.ylim([0, np.max(hold_g2)+0.5])
	plt.show()
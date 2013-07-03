import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

from scipy import integrate, interpolate, optimize
import numpy as np
import matplotlib.pyplot as plt
import constants as constants
from Experiment import Experiment

if __name__ == "__main__":
			
	hold_power = np.linspace(0.5, 1, num=60)
	hold_x = []
	hold_xx = []
	
	for power in hold_power:
		constants.power = power	
		experiment = Experiment(constants, Visualizer=False)
		experiment.run('power_dep')

		hold_x.append(experiment.spectrometer.x)
		hold_xx.append(experiment.spectrometer.xx)

	plt.plot(np.log10(hold_power), np.log10(hold_x), 'ro')
	plt.plot(np.log10(hold_power), np.log10(hold_xx), 'bo')

	idx = (np.abs(hold_power-1)).argmin()

	A = np.vstack([np.log10(hold_power[0:idx]), np.ones(len(np.log10(hold_power[0:idx])))]).T
	mx, cx = np.linalg.lstsq(A, np.log10(hold_x[0:idx]))[0]
	mxx, cxx = np.linalg.lstsq(A, np.log10(hold_xx[0:idx]))[0]

	print mx, mxx
	hold_power_interpolate = np.linspace(np.min(hold_power[0:idx]), np.max(hold_power[0:idx]), num=200)
	plt.plot(np.log10(hold_power_interpolate), mx*np.log10(hold_power_interpolate) + cx, 'r-')
	plt.plot(np.log10(hold_power_interpolate), mxx*np.log10(hold_power_interpolate) + cxx, 'b-')
	plt.legend(['X', 'XX'])
	plt.show()
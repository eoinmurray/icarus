import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

import time
import numpy as np
import matplotlib.pyplot as plt
import constants as constants
from Experiments import Experiment
import utils.save as save

def ideal_fidelity_lorentzian(s, tau, h):
	return 0.5*(1 + 1/(1 + ((s**2)*((tau*1e-9)**2))/(h**2)))

def fidelity(fss):
	print 'Starting fidelity measurement with fss: ', fss/1e-6, ' ueV'
	expected_fidelity = ideal_fidelity_lorentzian(constants.FSS, constants.xtau, constants.hbar)
	print 'Expecting fidelity of ', expected_fidelity, ' ueV'
	constants.FSS = fss

	HWPAngles = np.array([0, np.pi/8, None])
	QWPAngles = np.array([None, None, np.pi/4])
	hold_degrees_of_corrolation = []

	print 'Degrees of corrolation.'

	for i in xrange(HWPAngles.size):
		experiment = Experiment(constants, Visualizer = False)
		
		if HWPAngles[i] is not None:
			experiment.bench.setHWP(HWPAngles[i], HWPAngles[i])
			experiment.bench.setLabMatrix('NBSNBS HWPHWP SS PBSPBS')
		elif QWPAngles[i] is not None:
			experiment.bench.setQWP(QWPAngles[i], QWPAngles[i])
			experiment.bench.setLabMatrix('NBSNBS QWPQWP SS PBSPBS')
		
		experiment.run('basis')

		experiment.pcm.channel('D1D3').normalize(experiment.laser.pulse_width)
		experiment.pcm.channel('D1D4').normalize(experiment.laser.pulse_width)
		experiment.pcm.channel('D2D3').normalize(experiment.laser.pulse_width)
		experiment.pcm.channel('D2D4').normalize(experiment.laser.pulse_width)

		g2 = experiment.pcm.channel('D1D3').g2
		g2_cross = experiment.pcm.channel('D2D3').g2

		degree_of_corrolation = (g2 - g2_cross)/(g2 + g2_cross)

		hold_degrees_of_corrolation.append(degree_of_corrolation)


		name = 'linear'
		if i == 1:
			name = 'diag'
		elif i == 2:
			name = 'circ'
		
		f = np.around(constants.FSS/1e-6, decimals=2)
		g = np.around(constants.secondary_emission_probability, decimals=2)

		print '	', name, ': ', degree_of_corrolation		
		for key in experiment.pcm._channels:
			x = experiment.pcm._channels[key].bin_edges
			y = experiment.pcm._channels[key].counts
			save.savedata(x, y, name = name + ' ' + key, dir = 'fss-' + repr(f) + ' autog2-' + repr(g))

	grect = hold_degrees_of_corrolation[0]
	gdiag = hold_degrees_of_corrolation[1]
	gcirc = hold_degrees_of_corrolation[2]

	fidelity = (1 + grect + gdiag - gcirc)/4

	print 'fidelity: ', fidelity
	print 'real/expected: ', (fidelity/expected_fidelity)*100

	return fidelity


def average_fidelities():
	hold_f = []
	for i in xrange(10):
		t0 = time.time()
		f = fidelity(constants.FSS)
		t1 = time.time()
		total = t1-t0
		print 'time for fidelity run:', total
		print 'fidelity: ', f
		hold_f.append(f)

	print 'Average of fidelity run:', np.array(hold_f).mean()


if __name__ == "__main__":
	fidelity(constants.FSS)



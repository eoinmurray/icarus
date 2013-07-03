import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

import numpy as np
import matplotlib.pyplot as plt
import constants as constants_imp
from Experiments import Experiment

def fidelity(constants_rep = None, Visualizer = None):
	
	if constants_rep:
		constants = constants_rep
	else:
		constants = constants_imp

	HWPAngles = np.array([0, np.pi/8, None])
	QWPAngles = np.array([None, None, np.pi/4])
	hold_degrees_of_corrolation = []

	for i in xrange(HWPAngles.size):
	
		print 'i', i
		experiment = Experiment(constants, Visualizer = Visualizer)
		
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
		print degree_of_corrolation

		experiment.plot()
		name = 'linear'
		if i == 1:
			name = 'diag'
		elif i == 2:
			name = 'circ'
		
		experiment.visualizer.plt.savefig('out/2013-07-01/' + name + ' fss-' + repr(constants.FSS/1e-6) + ' autog2-' + repr(constants.secondary_emission_probability) + '.png')
		experiment.visualizer.plt.close()

	grect = hold_degrees_of_corrolation[0]
	gdiag = hold_degrees_of_corrolation[1]
	gcirc = hold_degrees_of_corrolation[2]

	fidelity = (1 + grect + gdiag - gcirc)/4

	return fidelity

if __name__ == "__main__":

	fss = np.linspace(0, 1, num=5)*1e-6
	autog2 = np.linspace(0, 1, num=5)

	for f in fss:
		for g in autog2:
			print f/1e-6, g 
			# constants_imp.FSS = f
			# constants_imp.secondary_emission_probability = g	
			# fidelity(constants_imp, Visualizer = False)


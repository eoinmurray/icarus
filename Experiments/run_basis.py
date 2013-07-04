

import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

import numpy as np
from Experiments import Experiment
import utils.save as save

def run_basis(angles, constants):

	experiment = Experiment(constants)
	
	HWPAngle, QWPAngle = angles
	if HWPAngle is not None:
		experiment.bench.setHWP(HWPAngle, HWPAngle)
		experiment.bench.setLabMatrix('NBSNBS HWPHWP SS PBSPBS')
	elif QWPAngle is not None:
		experiment.bench.setQWP(QWPAngle, QWPAngle)
		experiment.bench.setLabMatrix('NBSNBS QWPQWP SS PBSPBS')
	
	experiment.run('basis')
	
	f = np.around(constants.FSS/1e-6, decimals=2)
	
	name = 'linear'
	if HWPAngle == np.pi/8:
		name = 'diag'
	elif QWPAngle == np.pi/4:
		name = 'circ'
	
	for key in experiment.pcm._channels:
		x = experiment.pcm._channels[key].bin_edges
		y = experiment.pcm._channels[key].counts
		save.savedata(x, y, name = name + ' ' + key, dir = 'fss-' + repr(f) + ' xtau-' + repr(constants.xtau))

	experiment.pcm.channel('D1D3').normalize(experiment.laser.pulse_width)
	experiment.pcm.channel('D1D4').normalize(experiment.laser.pulse_width)
	experiment.pcm.channel('D2D3').normalize(experiment.laser.pulse_width)
	experiment.pcm.channel('D2D4').normalize(experiment.laser.pulse_width)

	g2 = experiment.pcm.channel('D1D3').g2
	g2_cross = experiment.pcm.channel('D2D3').g2
	
	degree_of_corrolation = (g2 - g2_cross)/(g2 + g2_cross)
	print '	', name, ': ', degree_of_corrolation		
	return degree_of_corrolation
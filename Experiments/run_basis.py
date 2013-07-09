

import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

import numpy as np
from Experiments import Experiment
from constants import Constants
import utils.save as save

def run_basis(angles, constants):

	experiment = Experiment(constants)
	
	if len(angles) == 2:
		HWPAngle, QWPAngle = angles
		HWPAngle2 = HWPAngle
		QWPAngle2 = QWPAngle
	else:
		HWPAngle, QWPAngle, HWPAngle2, QWPAngle2 = angles

	if HWPAngle is not None:
		experiment.bench.setHWP(HWPAngle, HWPAngle2)
		experiment.bench.setLabMatrix('NBSNBS HWPHWP SS PBSPBS')
	elif QWPAngle is not None:
		experiment.bench.setQWP(QWPAngle, QWPAngle2)
		experiment.bench.setLabMatrix('NBSNBS QWPQWP SS PBSPBS')
	
	if len(angles) == 4:
		experiment.bench.setLabMatrix('NBSNBS QWPQWP HWPHWP SS PBSPBS')

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

	return degree_of_corrolation


def plotres(name, constants):
	f = np.around(constants.FSS/1e-6, decimals=2)	
	plt=save.plotdata(
		name=name, 
		dir='fss-'+repr(f)+' xtau-'+repr(constants.xtau)
	)

	plt.show()


if __name__ == "__main__":
	constants = Constants()
	angles = [np.pi/8, None]
	name = 'diag'

	print name, 'degree of corrolation.'
	degree_of_corrolation = run_basis(angles, constants)
	print degree_of_corrolation

	plotres(name, constants)
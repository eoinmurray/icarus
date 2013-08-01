


import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
import numpy as np
from constants import Constants
import utils.save as save
import Icarus.Experiment as Experiment	



def run_basis(angles, constants, dirname):
	"""
		Runs crosscorrlation vs wave plartes experiment.
	"""
	
	experiment = Experiment(constants)
	
	if len(angles) == 2:
		HWPAngle, QWPAngle = angles
		HWPAngle2 = HWPAngle
		QWPAngle2 = QWPAngle
	else:
		HWPAngle, QWPAngle, HWPAngle2, QWPAngle2 = angles

	if len(angles) == 4:
		experiment.bench.setHWP(HWPAngle, HWPAngle2)
		experiment.bench.setQWP(QWPAngle, QWPAngle2)
		experiment.bench.setLabMatrix('NBSNBS QWPQWP HWPHWP SS PBSPBS')
	elif (HWPAngle is not None):
		experiment.bench.setHWP(HWPAngle, HWPAngle2)
		experiment.bench.setLabMatrix('NBSNBS HWPHWP SS PBSPBS')
	elif (QWPAngle is not None):
		experiment.bench.setQWP(QWPAngle, QWPAngle2)
		experiment.bench.setLabMatrix('NBSNBS QWPQWP SS PBSPBS')
	
	experiment.run('basis')
	
	f = np.around(constants.FSS/1e-6, decimals=2)
	name = 'linear'
	if HWPAngle == np.pi/8:
		name = 'diag'
	elif QWPAngle == np.pi/4:
		name = 'circ'
	

	f = np.around(constants.FSS/1e-6, decimals=2)

	save.save_params(dirname)

	for key in experiment.pcm._channels:
		x = experiment.pcm._channels[key].bin_edges
		y = experiment.pcm._channels[key].counts
		save.savedata(x, y, name = name + ' ' + key, dir = dirname)


	plt = save.plotdata(name = name, dir = dirname)
	save.savefig(plt, name = name, dir = dirname)
	plt.close('all')

	experiment.pcm.channel('D1D3').normalize(experiment.laser.pulse_width)
	experiment.pcm.channel('D1D4').normalize(experiment.laser.pulse_width)
	experiment.pcm.channel('D2D3').normalize(experiment.laser.pulse_width)
	experiment.pcm.channel('D2D4').normalize(experiment.laser.pulse_width)

	g2 = experiment.pcm.channel('D1D3').g2
	g2_cross = experiment.pcm.channel('D1D4').g2

	g21 = experiment.pcm.channel('D2D3').g2
	g2_cross1 = experiment.pcm.channel('D2D4').g2

	if len(angles) == 4:
		if g2 == 0:
			ret = 0
		else:
			ret = g2 / (g2 + g2_cross)
	else:
		ret = (g2 - g2_cross) / (g2 + g2_cross)
	
	return ret



def plotres(name, constants):
	"""
		Plots the result of the basis experiment.
	"""

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


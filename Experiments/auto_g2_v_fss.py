


import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
import numpy as np
from constants import Constants
import utils.save as save
import Icarus.Experiment as Experiment	
import time
from multiprocessing import Pool
import matplotlib.pyplot as plt


def run_basis(FSS):
	"""
		Runs crosscorrlation vs wave plartes experiment.
	"""
	
	print 'Running diag basis with FSS', FSS.astype('|S4').tostring()

	constants = Constants()
	constants.FSS = FSS
	experiment = Experiment(constants)
	
	experiment.bench.setHWP(np.pi/8, np.pi/8)
	experiment.bench.setLabMatrix('NBSNBS HWPHWP SS PBSPBS')
	
	experiment.run('basis')
	
	experiment.pcm.channel('D1D3').normalize(experiment.laser.pulse_width)
	experiment.pcm.channel('D1D4').normalize(experiment.laser.pulse_width)
	experiment.pcm.channel('D2D3').normalize(experiment.laser.pulse_width)
	experiment.pcm.channel('D2D4').normalize(experiment.laser.pulse_width)

	
	for key in experiment.pcm._channels:
		x = experiment.pcm._channels[key].bin_edges
		y = experiment.pcm._channels[key].counts
		save.savedata(x, y, name = 'diag' + '_' + key + '_' + FSS.astype('|S4').tostring(), dir = 'auto_g2_v_fss_dephase2.5e10secondaty0.18')

	g2 = experiment.pcm.channel('D1D3').g2
	g2_cross = experiment.pcm.channel('D1D4').g2

	return g2_cross

def auto_g2_v_fss():
	"""
		Runs the fidelity experiment versus FSS.	
	"""

	fss = np.linspace(0, 10, 50)
	fss = fss*1e-6

	pool = Pool(processes=4)  
	hold_g2 = pool.map(run_basis, fss) 

	plt.plot(fss/1e-6, hold_g2)
	save.savefig(plt, name="auto_g2_v_fss_dephase2.5e10secondaty0.18")
	save.savedata(fss/1e-6, hold_g2, name='auto_g2_v_fidelity', dir = 'auto_g2_v_fss_dephase2.5e10secondaty0.18')
	plt.show()
	
if __name__ == "__main__":
	auto_g2_v_fss()	


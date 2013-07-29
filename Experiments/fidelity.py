


import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
import functools
import time
from multiprocessing import Pool
import numpy as np
import matplotlib.pyplot as plt
from constants import Constants
from run_basis import run_basis
import utils.save as save
from Icarus.Classes.QuantumDot import QuantumDot



def fidelity(FSS = None):
	"""
		Run three basis corrlations and calculates fidelity.
	"""

	constants = Constants()

	if FSS:
		print 'FSS passed.'
		constants.FSS = FSS

	indication_qd = QuantumDot(constants.xtau, constants.xxtau, constants.ptau, constants.FSS, constants.crosstau)
	expected_fidelity, first_order_coherence = indication_qd.ideal_fidelity_lorentzian()
	
	print 'Starting fidelity measurement with fss: ', constants.FSS/1e-6, 'ueV and xlifetime of ', constants.xtau, 'ns'
	print 'Expecting fidelity of ', np.around(expected_fidelity, decimals=2)
	print 'First order coherence ', np.around(first_order_coherence, decimals=2)

	if constants.secondary_emission_probability != 0.0:
		print 'NOTE: secondary_emission_probability is non-zero.'
	
	names = ['linear', 'diag', 'circ']
	HWPAngles = np.array([0, np.pi/8, None])
	QWPAngles = np.array([None, None, np.pi/4])
	angles = np.vstack((HWPAngles, QWPAngles)).T	
	

	hold_degrees_of_corrolation = []


	if __name__ == "__main__":

		print 'Running from main, starting multiprocessing.'
		pool = Pool(processes=4)
		hold_degrees_of_corrolation = pool.map(functools.partial(run_basis, constants=constants), angles)

	else:

		hold_degrees_of_corrolation.append(run_basis(angles[0], constants) )
		hold_degrees_of_corrolation.append(run_basis(angles[1], constants) )
		hold_degrees_of_corrolation.append(run_basis(angles[2], constants) )
		

	grect = hold_degrees_of_corrolation[0]
	gdiag = hold_degrees_of_corrolation[1]
	gcirc = hold_degrees_of_corrolation[2]
	fidelity = (1 + grect + gdiag - gcirc)/4


	print 'Degrees of corrolation.'
	print '	linear:   ', grect
	print '	diagonal: ', gdiag
	print '	circular: ', gcirc
	print 'fidelity: ', np.around(fidelity, decimals=2)
	print 'real/expected: ', (fidelity/expected_fidelity)*100, '%'

	
	f = np.around(constants.FSS/1e-6, decimals=2)
	dirname = 'fss-' + repr(f) + ' xtau-' + repr(constants.xtau)	

	for name in names:	

		plt = save.plotdata(name = name, dir = dirname)
		if __name__ == "__main__":
			plt.show()
		save.savefig(plt, name = name, dir = dirname)
		plt.close('all')

	return fidelity



if __name__ == "__main__":	
	fidelity()


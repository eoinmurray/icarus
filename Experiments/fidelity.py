

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

def ideal_fidelity_lorentzian(fss, xlifetime, h):
	"""Returns ideal fidelty, from AH thesis."""
	return 0.5*(1 + 1/(1 + ((fss**2)*((xlifetime*1e-9)**2))/(h**2)))

def fidelity_multi_process():
	constants = Constants()
	
	expected_fidelity = ideal_fidelity_lorentzian(constants.FSS, constants.xtau, constants.hbar)
	print 'Starting fidelity measurement with fss: ', FSS/1e-6, 'ueV and xlifetime of ', constants.xtau, 'ns'
	print 'Expecting fidelity of ', expected_fidelity
	
	names = ['linear', 'diag', 'circ']
	HWPAngles = np.array([0, np.pi/8, None])
	QWPAngles = np.array([None, None, np.pi/4])
	angles = np.vstack((HWPAngles, QWPAngles)).T
	
	print 'Degrees of corrolation.'
	pool = Pool(processes=4)  
	hold_degrees_of_corrolation = []
	hold_degrees_of_corrolation = pool.map(functools.partial(run_basis, constants=constants), angles)
	
	f = np.around(constants.FSS/1e-6, decimals=2)
	dirname = 'fss-' + repr(f) + ' xtau-' + repr(constants.xtau)	
	for name in names:	
		plt = save.plotdata(name = name, dir = dirname)
		save.savefig(plt, name = name, dir = dirname)

	grect = hold_degrees_of_corrolation[0]
	gdiag = hold_degrees_of_corrolation[1]
	gcirc = hold_degrees_of_corrolation[2]
	fidelity = (1 + grect + gdiag - gcirc)/4

	print 'fidelity: ', fidelity
	print 'real/expected: ', (fidelity/expected_fidelity)*100, '%'
	return fidelity

def fidelity_single_process(fss):
	constants = Constants()
	constants.FSS = fss
	print 'Starting fidelity measurement with fss: ', fss/1e-6, ' ueV'
	expected_fidelity = ideal_fidelity_lorentzian(constants.FSS, constants.xtau, constants.hbar)
	print 'Expecting fidelity of ', expected_fidelity
	
	HWPAngles = np.array([0, np.pi/8, None])
	QWPAngles = np.array([None, None, np.pi/4])
	angles = np.vstack((HWPAngles, QWPAngles)).T
	hold_degrees_of_corrolation = []
	
	print 'Degrees of corrolation.'
	hold_degrees_of_corrolation.append(run_basis(angles[0], constants) )
	hold_degrees_of_corrolation.append(run_basis(angles[1], constants) )
	hold_degrees_of_corrolation.append(run_basis(angles[2], constants) )

	grect = hold_degrees_of_corrolation[0]
	gdiag = hold_degrees_of_corrolation[1]
	gcirc = hold_degrees_of_corrolation[2]
	fidelity = (1 + grect + gdiag - gcirc)/4

	print 'fidelity: ', fidelity
	print 'real/expected: ', (fidelity/expected_fidelity)*100
	return fidelity

if __name__ == "__main__":	
	fidelity_multi_process()


import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

import functools
import time
from multiprocessing import Pool
import numpy as np
import matplotlib.pyplot as plt
import constants as Constants
from run_basis import run_basis

def ideal_fidelity_lorentzian(s, tau, h):
	return 0.5*(1 + 1/(1 + ((s**2)*((tau*1e-9)**2))/(h**2)))

def fidelity_single_process(fss):
	constants = Constants.Constants()
	constants.FSS = fss
	print 'Starting fidelity measurement with fss: ', fss/1e-6, ' ueV'
	expected_fidelity = ideal_fidelity_lorentzian(constants.FSS, constants.xtau, constants.hbar)
	print 'Expecting fidelity of ', expected_fidelity, ' ueV'
	
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

def fidelity_multi_process(fss):
	constants = Constants.Constants()

	print 'Starting fidelity measurement with fss: ', fss/1e-6, ' ueV'
	expected_fidelity = ideal_fidelity_lorentzian(constants.FSS, constants.xtau, constants.hbar)
	print 'Expecting fidelity of ', expected_fidelity, ' ueV'
	
	HWPAngles = np.array([0, np.pi/8, None])
	QWPAngles = np.array([None, None, np.pi/4])
	angles = np.vstack((HWPAngles, QWPAngles)).T
	hold_degrees_of_corrolation = []
	constants.FSS = fss
	print 'Degrees of corrolation.'
	pool = Pool(processes=4)  

	hold_degrees_of_corrolation = pool.map(functools.partial(run_basis, constants=constants), angles) 

	grect = hold_degrees_of_corrolation[0]
	gdiag = hold_degrees_of_corrolation[1]
	gcirc = hold_degrees_of_corrolation[2]
	fidelity = (1 + grect + gdiag - gcirc)/4

	print 'fidelity: ', fidelity
	print 'real/expected: ', (fidelity/expected_fidelity)*100
	return fidelity


if __name__ == "__main__":
	constants = Constants.Constants()	
	fidelity_multi_process(constants.FSS)

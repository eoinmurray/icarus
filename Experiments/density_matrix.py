

import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

import numpy as np
import matplotlib.pyplot as plt
import utils.save as save
from constants import Constants
from run_basis import run_basis
from utils.density_matrix_sim_deps import *
import functools
import time
from multiprocessing import Pool

def density_matrix_sim():
	constants = Constants()

	names = ['linear', 'diag', 'circ']
	HWPAngles = np.array([0, np.pi/8, None])
	QWPAngles = np.array([None, None, np.pi/4])
	angles = np.vstack((HWPAngles, QWPAngles)).T	
	
	if __name__ == "__main__":
		print 'Running from main, starting multiprocessing.'
		pool = Pool(processes=4)
		res = pool.map(functools.partial(run_basis, constants=constants), measurements)
	
	res = 0.25*np.array(res)
	
	density_matrix = res[0]*M1 + res[1]*M2 + res[2]*M3 + res[3]*M4 + res[4]*M5 + res[5]*M6 + res[6]*M7 + res[7]*M8 + res[8]*M9 + res[9]*M10 + res[10]*M11 + res[11]*M12 + res[12]*M13 + res[13]*M14 + res[14]*M15 + res[15]*M16

	tol = 1e-15
	density_matrix.real[abs(density_matrix.real) < tol] = 0.0
	density_matrix.imag[abs(density_matrix.imag) < tol] = 0.0

	plt = save.plot_matrix(
		np.real(density_matrix),
		'$Re(\\rho)$'
	)
	plt.show()

if __name__ == "__main__":
	density_matrix_sim()
	
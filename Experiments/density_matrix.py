


import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) ; sys.path.insert(0,parentdir)
import functools
import time
from multiprocessing import Pool
import numpy as np
import matplotlib.pyplot as plt
import utils.save as save
from constants import Constants
from run_basis import run_basis
from utils.density_matrix_sim_deps import *



def density_matrix_sim():
	"""
		Calculates the biphoton density matrix.
	"""

	constants = Constants()

	names = ['linear', 'diag', 'circ']
	HWPAngles = np.array([0, np.pi/8, None])
	QWPAngles = np.array([None, None, np.pi/4])
	angles = np.vstack((HWPAngles, QWPAngles)).T	
	
	pool = Pool(processes=4)
	res = np.array(pool.map(functools.partial(run_basis, constants=constants), measurements))
	
	print res

	density_matrix = res[0]*M1 + res[1]*M2 + res[2]*M3 + res[3]*M4 + res[4]*M5 + res[5]*M6 + res[6]*M7 + res[7]*M8 + res[8]*M9 + res[9]*M10 + res[10]*M11 + res[11]*M12 + res[12]*M13 + res[13]*M14 + res[14]*M15 + res[15]*M16
	density_matrix = np.squeeze(np.asmatrix(density_matrix))
	
	print 'Density Matrix'
	print np.real(density_matrix)
	print np.imag(density_matrix)

	f = np.around(constants.FSS/1e-6, decimals=2)
	
	plt_real = save.plot_matrix(
		np.real(density_matrix),
		'$Re(\\rho)$, F ' + repr(f) + '$\mu eV$'
	)
	save.savefig(plt_real, name='DensityMatrixReal-f-' + repr(f))

	plt_imag = save.plot_matrix(
		np.imag(density_matrix),
		'$Im(\\rho)$, F ' + repr(f) + '$\mu eV$'
	)

	save.savefig(plt_imag, name='DensityMatrixImag-f-' + repr(f))
	plt_real.show()
	plt_imag.show()

	print 'fidelity: ', np.real(density_matrix[0,0])+np.real(density_matrix[3,0])



if __name__ == "__main__":
	density_matrix_sim()
	
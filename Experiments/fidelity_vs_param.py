



import time
import functools as functools
from multiprocessing import Pool
import numpy as np
import matplotlib.pyplot as plt
from fidelity import fidelity
import utils.save as save
import functools



def fidelity_vs_param():
	"""
		Runs the fidelity experiment versus FSS.	
	"""


	folder_name = 'fid_v_bg'
	param_array = np.linspace( 0., 0.5, 20)
	attr_name = 'bg_emission_rate'

	pool = Pool(processes=4)

	save.ensure_exists(folder_name)
	hold_fidelity =	pool.map(functools.partial(fidelity, attr_name = attr_name, folder_name = folder_name), param_array)

	if __name__ == "__main__":
		plt.plot(param_array, hold_fidelity)
		plt.show()

if __name__ == "__main__":
	fidelity_vs_param()


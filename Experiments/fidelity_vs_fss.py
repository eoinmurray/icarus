


import time
from multiprocessing import Pool
import numpy as np
import matplotlib.pyplot as plt
from fidelity import fidelity
import utils.save as save



def fidelity_vs_fss():
	"""
		Runs the fidelity experiment versus FSS.	
	"""

	fss = np.linspace( -10, 10, 150)
	fss = fss*1e-6

	pool = Pool(processes=4)  
	hold_fidelity = pool.map(fidelity, fss) 

	plt.plot(fss/1e-6, hold_fidelity)
	save.savefig(plt, name="fss_v_fidelity")
	save.savedata(fss/1e-6, hold_fidelity, name='fss_v_fidelity')



if __name__ == "__main__":
	fidelity_vs_fss()




import time
from multiprocessing import Pool
import numpy as np
import matplotlib.pyplot as plt
from fidelity import fidelity
import utils.save as save

def fidelity_vs_fss():

	size = 70
	fss = np.concatenate( (np.linspace( -10, 0, num=size), np.linspace( 0, 10, num=size)), axis=0)
	fss = fss*1e-6

	pool = Pool(processes=4)  
	hold_fidelity = pool.map(fidelity, fss) 

	plt.plot(fss/1e-6, hold_fidelity)
	save.savefig(plt, name="fss_v_fidelity")
	save.savedata(fss/1e-6, hold_fidelity, name='fss_v_fidelity')

if __name__ == "__main__":
	fidelity_vs_fss()


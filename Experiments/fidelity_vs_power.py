


import time
from multiprocessing import Pool
import numpy as np
import matplotlib.pyplot as plt
from fidelity import fidelity
import utils.save as save



def fidelity_vs_power():
	"""
		Runs the fidelity experiment versus power.	
	"""

	power = np.linspace(0.2, 4, 10)

	pool = Pool(processes=4)  
	hold_fidelity = pool.map(fidelity, power) 

	print hold_fidelity

	plt.plot(power, hold_fidelity)
	save.savefig(plt, name="power_v_fidelity")
	save.savedata(power, hold_fidelity, name='power_v_fidelity')
	plt.show()



if __name__ == "__main__":
	fidelity_vs_power()

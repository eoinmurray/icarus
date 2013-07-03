import numpy as np
import matplotlib.pyplot as plt
from fidelity import fidelity
import utils.save as save
import constants as constants

def fidelity_vs_fss():

	fss = np.linspace( -5, 5, num=50)*1e-6
	hold_fidelity = []
	
	for f in fss:
		constants.FSS = f
		hold_fidelity.append(fidelity(constants))

	plt.plot(fss/1e-6, hold_fidelity)
	save.savefig(plt, name="fss_v_fidelity")
	save.savedata(fss/1e-6, hold_fidelity, name='fss_v_fidelity')

if __name__ == "__main__":
	fidelity_vs_fss()
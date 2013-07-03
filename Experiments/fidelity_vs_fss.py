import numpy as np
import matplotlib.pyplot as plt
from fidelity import fidelity
import constants as constants

def fidelity_vs_fss():

	fss = np.linspace( -5, 5, num=10)*1e-6
	hold_fidelity = []
	
	for f in fss:
		constants.FSS = f
		hold_fidelity.append(fidelity(constants))

	print fss
	print hold_fidelity

	plt.plot(fss/1e-6, hold_fidelity)
	plt.show()

if __name__ == "__main__":
	fidelity_vs_fss()
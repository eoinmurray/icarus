import numpy as np
import matplotlib.pyplot as plt
from fidelity import fidelity
import utils.save as save
import constants as constants

def fidelity_vs_auto_g2():

	constants.secondary_emission = True
	constants.secondary_emission_degree = 1
	secondary_emission_probabilitys = np.linspace(0, 1, num=50)
	hold_fidelity = []
	
	for secondary_emission_probability in secondary_emission_probabilitys:
		constants.secondary_emission_probability = secondary_emission_probability
		hold_fidelity.append(fidelity(constants))

	print hold_fidelity
	plt.plot(secondary_emission_probabilitys, hold_fidelity)
	plt.xlabel('auto-g2, FSS: '+ repr(constants.FSS))
	plt.ylabel('Fidelity')
	f = np.around(constants.FSS/1e-6, decimals=2)
	g = np.around(constants.secondary_emission_probability, decimals=2)
	save.savefig(plt, name = 'fidelity_vs_g2', dir = 'fss-' + repr(f) + ' autog2-' + repr(g))

if __name__ == "__main__":
	
	fidelity_vs_auto_g2()
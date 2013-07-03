import numpy as np
import matplotlib.pyplot as plt
from fidelity import fidelity
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
	plt.savefig('out/2013-07-01/' + 'fidelity_vs_g2_fss-' + repr(constants.FSS) + '.png')

if __name__ == "__main__":
	
	fidelity_vs_auto_g2()
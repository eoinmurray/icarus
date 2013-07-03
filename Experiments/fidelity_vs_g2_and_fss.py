import numpy as np
import matplotlib.pyplot as plt
from fidelity import fidelity
import constants as constants

def app():	
	fss = np.linspace(0, 1, num=5)*1e-6
	autog2 = np.linspace(0, 1, num=5)

	for f in fss:
		for g in autog2:
			print f/1e-6, g 
			# constants_imp.FSS = f
			# constants_imp.secondary_emission_probability = g	
			# fidelity(constants_imp, Visualizer = False)

if __name__ == "__main__":
	app()
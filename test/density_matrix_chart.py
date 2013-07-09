

import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

import Experiments.utils.save as save

if __name__ == "__main__":
	x = np.real(np.array([
					[0.5,0,0,0.5],
					[0,0,0,0],
					[0,0,0,0],
					[0.5,0,0,0.5]
				]))
	print x[0]
	save.plot_matrix(
		x,
		title = '$Re(\\rho)$'
	)
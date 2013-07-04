

import numpy as np 
import matplotlib.pyplot as plt

def lifetimes_free(xtau):
	"""Returns lifetimes where xlifetime can be less than xxlifetime"""
	xlifetime = np.random.exponential(xtau, size=1)[0]
	xxlifetime = np.random.exponential(xtau/2, size=1)[0]
	return xlifetime, xxlifetime

def lifetimes_constrained(xtau):
	"""Returns lifetimes where xlifetime **cannot** be less than xxlifetime"""
	xlifetime = 1
	xxlifetime = 10
	while xlifetime < xxlifetime:
		xlifetime = np.random.exponential( xtau, 1)[0]
		xxlifetime = np.random.exponential( xtau/2, 1)[0]
	return xlifetime, xxlifetime

def test():
	size = 100000
	xtau = 1.
	FSS = np.linspace(0, 4, num=100)*1e-6
	hbar = 6.56e-16

	lifetimes = np.array([lifetimes_constrained(xtau) for i in xrange(size)])
	xlifetimes = lifetimes[:, 0]
	xxlifetimes = lifetimes[:, 1]
	
	bins = np.linspace(0, 7, num=1000)
	xcounts, bin_edges = np.histogram(xlifetimes, bins)
	xxcounts, bin_edges = np.histogram(xxlifetimes, bins)

	bin_edges = bin_edges[0 : bin_edges.size - 1]

	plt.plot(bin_edges, xcounts)
	plt.plot(bin_edges, xxcounts)
	plt.show()

if __name__ == "__main__":
	test()
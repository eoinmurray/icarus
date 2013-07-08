

import numpy as np 
import matplotlib.pyplot as plt

def smooth(array, num_points):
	length = np.floor(array.size/num_points)
	smoothed_array = np.zeros(length)
  	i = 0
	
	while i != length:
		segment = array[i*num_points: (i+1)*num_points]
		smoothed_array[i] = np.mean(segment)
		i = i + 1
    
	return smoothed_array

def x_probability(mean_photon_num):
	return 1 - np.exp(- mean_photon_num)

def xx_probability(mean_photon_num):		
	return 1 - (1+ mean_photon_num)*np.exp(- mean_photon_num)

def lifetimes_free(xtau, mean_photon_num):
	"""Returns lifetimes where xlifetime can be less than xxlifetime"""
	
	if np.random.random_sample() < xx_probability(mean_photon_num):
		xlifetime = np.random.exponential(xtau, 1)[0]
		xxlifetime = np.random.exponential(xtau/2, 1)[0]
	
	elif np.random.random_sample() < x_probability(mean_photon_num):
		xlifetime = np.random.exponential(xtau, 1)[0]
		xxlifetime = 1e6
	
	else:
		xlifetime = 1e6
		xxlifetime = 1e6
	
	return xlifetime, xxlifetime

def lifetimes_constrained_xx(xtau, mean_photon_num):
	"""Returns lifetimes where xlifetime **cannot** be less than xxlifetime"""
	
	if np.random.random_sample() < xx_probability(mean_photon_num):
	
		xlifetime = np.random.exponential( xtau, 1)[0]
		xxlifetime = np.random.exponential( xtau, 1)[0]
	
		while xxlifetime > xlifetime:
			xxlifetime = np.random.exponential( xtau, 1)[0]
	
	elif np.random.random_sample() < x_probability(mean_photon_num):
		xlifetime = np.random.exponential(xtau, 1)[0]
		xxlifetime = 1e6
	
	else:
		xlifetime = 1e6
		xxlifetime = 1e6
	
	return xlifetime, xxlifetime


def test():
	size = 60000
	xtau = 1.
	FSS = np.linspace(0, 4, num=100)*1e-6
	hbar = 6.56e-16
	mean_photon_num = 10

	lifetimes_f = np.array([lifetimes_free(xtau, mean_photon_num) for i in xrange(size)])
	lifetimes_c_xx = np.array([lifetimes_constrained_xx(xtau, mean_photon_num) for i in xrange(size)])

	xlifetimes_free = lifetimes_f[:, 0]
	xxlifetimes_free = lifetimes_f[:, 1]	
	xlifetimes_constrained_xx = lifetimes_c_xx[:, 0]
	xxlifetimes_constrained_xx = lifetimes_c_xx[:, 1]

	bins = np.linspace(0, 7, num=1000)
	xcounts_free, bin_edges = np.histogram(xlifetimes_free, bins)
	xxcounts_free, bin_edges = np.histogram(xxlifetimes_free, bins)
	xcounts_constrained_xx, bin_edges = np.histogram(xlifetimes_constrained_xx, bins)
	xxcounts_constrained_xx, bin_edges = np.histogram(xxlifetimes_constrained_xx, bins)
	bin_edges = bin_edges[0 : bin_edges.size - 1]

	fig = plt.subplot(111)
	
	
	fig.plot(bin_edges, xxcounts_constrained_xx)
	fig.plot(bin_edges, xcounts_constrained_xx)
	fig.plot(smooth(bin_edges, 3), smooth(xcounts_free, 3))
	fig.plot(smooth(bin_edges, 3), smooth(xxcounts_free, 3))
	
	fig.set_ylabel('counts')
	fig.set_xlabel('time (ns)')

	fig.legend(['xx_c', 'x_c', 'x_f', 'xx_f'])
	plt.show()

if __name__ == "__main__":
	test()



import numpy as np



class Constants():
	"""
		Class of constants, duh.
	"""

	# Quantum dot
	xtau = 1.
	xxtau = 0.5
	ptau = 2.
	crosstau = 2.5
	poptime_on = False
	FSS = 1.e-6
	hbar = 6.58e-16
	secondary_emission_probability = 0.

	# Laser
	pulse_width = 25.
	power = 0.7

	# Detector
	FWHM = 4.8
	sigma = FWHM/(2*np.sqrt(np.log(2)*2))
	efficiency = 1
	delay = 161.8
	bin_width = 50

	# Experiment parameters
	num_iterations = 1
	integration_time = 400000
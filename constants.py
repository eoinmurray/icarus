


import numpy as np



class Constants():
	"""
		Class of constants, duh.
	"""

	# Quantum dot
	xtau = 1.
	xxtau = 0.5
	ptau = 2.
	poptime_on = False
	hbar = 6.58e-16
	
	FSS = 0.e-6
	crosstau = 2.5e10
	secondary_emission_probability = 0.2
	background_light_rate = 0.05

	# Laser
	pulse_width = 25.
	power = 0.8

	# Detector
	FWHM = 4.8
	sigma = FWHM/(2*np.sqrt(np.log(2)*2))
	efficiency = 1
	delay = 161.8
	bin_width = 50

	# Experiment parameters
	num_iterations = 1
	integration_time = 100000
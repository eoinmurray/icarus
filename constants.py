import numpy as np
# All times in nanoseconds
# In real experiment integration time is 0.5e9ns, but detector yield is also much much lower.

# Quantum dot
class Constants():
	xtau = 1
	xxtau = 0.5
	ptau = 2
	poptime = False
	FSS = 1e-6
	hbar = 6.58e-16
	secondary_emission = False
	secondary_emission_probability = 0.2
	secondary_emission_degree = 1

	# Laser
	pulse_width = 25.
	power = 0.1

	# Detector
	FWHM = 4.8
	sigma = FWHM/(2*np.sqrt(np.log(2)*2))
	sigma = 0
	efficiency = 1
	delay = 161.8
	bin_width = 50

	# Experiment parameters
	num_iterations = 100
	integration_time = 2000
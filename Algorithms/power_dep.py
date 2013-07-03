import numpy as np

def power_dep(qd, pcm, laser, bench, spectrometer, constants):
	
	for time in laser.pulseTimes(constants.integration_time):
	
		xxtrue, xtrue = qd.emission(laser.power)
		xlifetime, xxlifetime = qd.lifetimes()
		poptime = np.random.exponential( constants.ptau - constants.xtau, size=1)[0]
		
		if xxtrue:
			spectrometer.hit('XX')

		if xtrue:
			spectrometer.hit('X')
			
			if np.random.random_sample() < constants.secondary_emission_probability*qd.x_probability(laser.power**constants.secondary_emission_degree):
				spectrometer.hit('X')
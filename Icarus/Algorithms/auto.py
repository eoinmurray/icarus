


import numpy as np



def auto(qd, pcm, laser, bench, spectrometer, constants):
	"""
		Autocorrolation experiment algorithm.
	"""


	for time in laser.pulseTimes(constants.integration_time):

		xxtrue, xtrue = qd.emission(laser.power) 
		xlifetime, xxlifetime = qd.generate_lifetimes()
		poptime = qd.poptime()
		
		if not constants.poptime_on:
			poptime = 0

		if xtrue:
			if np.random.random_sample() < 0.5:
				pcm.detector('D3').hit(time, xlifetime + poptime)
			else:
				pcm.detector('D1').hit(time, xlifetime + poptime)			
		
			xxtrue, xtrue = qd.emission(laser.power*constants.secondary_emission_probability) 
			time_2 = time + xlifetime + poptime
			xlifetime, xxlifetime = qd.generate_lifetimes()
			poptime = qd.poptime()
						
			if not constants.poptime_on:
				poptime = 0
		
			if xtrue:
				if np.random.random_sample() < 0.5:
					pcm.detector('D3').hit(time_2, xlifetime + poptime)
				else:
					pcm.detector('D1').hit(time_2, xlifetime + poptime)
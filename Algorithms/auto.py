import numpy as np

def auto(qd, pcm, laser, bench, spectrometer, constants):
	
	for time in laser.pulseTimes(constants.integration_time):
	
		xlifetime, xxlifetime = qd.lifetimes()
		poptime = np.random.exponential( constants.ptau - constants.xtau, size=1)[0]
		if not constants.poptime:
			poptime = 0

		xtrue = np.random.random_sample() < qd.x_probability(laser.power)

		if xtrue:
			
			if np.random.random_sample() < 0.5:
				pcm.detector('D3').hit(time, xlifetime + poptime)
			else:
				pcm.detector('D1').hit(time, xlifetime + poptime)
			
			if constants.secondary_emission:
			
				time_2 = time + xlifetime + poptime
				xlifetime, xxlifetime = qd.lifetimes()
				poptime = np.random.exponential( constants.ptau - constants.xtau, size=1)[0]
				if not constants.poptime:
					poptime = 0
			
				xtrue = np.random.random_sample() < qd.x_probability(laser.power*constants.secondary_emission_probability)
				
				if xtrue:
					if np.random.random_sample() < 0.5:
						pcm.detector('D3').hit(time_2, xlifetime + poptime)
					else:
						pcm.detector('D1').hit(time_2, xlifetime + poptime)
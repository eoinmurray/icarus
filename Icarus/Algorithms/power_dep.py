

import numpy as np

def power_dep(qd, pcm, laser, bench, spectrometer, constants):

	for time in laser.pulseTimes(constants.integration_time):	
		xxtrue, xtrue = qd.emission(laser.power) 
		xlifetime, xxlifetime = qd.lifetimes()
		poptime = qd.poptime()
		
		if not constants.poptime_on:
			poptime = 0

		if xxtrue:
			spectrometer.hit('XX')

		if xtrue:
			spectrometer.hit('X')

			if constants.secondary_emission:
			
				xxtrue, xtrue = qd.emission(laser.power*constants.secondary_emission_probability) 
				time_2 = time + xlifetime + poptime
				xlifetime, xxlifetime = qd.lifetimes()
				poptime = qd.poptime()
							
				if not constants.poptime_on:
					poptime = 0
			
				if xtrue:
					spectrometer.hit('X')

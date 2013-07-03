import numpy as np

def cross(qd, pcm, laser, bench, spectrometer, constants):
	
	for time in laser.pulseTimes(constants.integration_time):	
		xxtrue, xtrue = qd.emission(laser.power)
		xlifetime, xxlifetime = qd.lifetimes()
		
		if xxtrue:
			pcm.detector('D3').hit(time, xxlifetime)

		if xtrue:	
			pcm.detector('D1').hit(time, xlifetime)

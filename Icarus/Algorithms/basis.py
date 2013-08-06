


import numpy as np



def basis(qd, pcm, laser, bench, spectrometer, constants):
	"""
		Polarisation dependant cross corrolation experiment algorithm.
	"""

	for time in laser.pulseTimes(constants.integration_time):

		# QD emission

		xxtrue, xtrue = qd.emission(laser.power) 
		xlifetime, xxlifetime = qd.generate_lifetimes()
		poptime = qd.poptime()
	
		if not constants.poptime_on:
			poptime = 0
		
		xemission_time = xlifetime + poptime
		xxemission_time = xxlifetime + poptime

		state = qd.generate_state()
		propogated_state = bench.matrix*state

		D1D3_prob = pcm.channel('D1D3').calculate_probability(propogated_state)
		D1D4_prob = pcm.channel('D1D4').calculate_probability(propogated_state)
		D2D3_prob = pcm.channel('D2D3').calculate_probability(propogated_state)
		D2D4_prob = pcm.channel('D2D4').calculate_probability(propogated_state)

		prob = np.array([D1D3_prob, D1D4_prob, D2D3_prob, D2D4_prob])
		boole = (prob.cumsum() > np.random.random_sample() )
		
		xxfirst_match = np.where(boole ==True)[0][0] 
		xfirst_match = xxfirst_match

		k = 1. - constants.bg_emission_rate
		bg_emission_time = np.random.exponential(constants.bg_emission_rate, 1)[0]

		if np.random.random_sample() < (1.- k)/2.:
			
			boole = ( (np.ones(4) * 0.25 ).cumsum() > np.random.random_sample() )
			rand_first_match = np.where(boole ==True)[0][0] 

			if xxtrue:
				xxemission_time = bg_emission_time
				xxfirst_match = rand_first_match
			else:
				xemission_time = bg_emission_time
				xfirst_match = rand_first_match

		if np.random.random_sample() < (1.- k)/2.:
			boole = ( (np.ones(4) * 0.25 ).cumsum() > np.random.random_sample() )
			rand_first_match = np.where(boole ==True)[0][0] 
			xemission_time = bg_emission_time
			xfirst_match = rand_first_match

		if xxtrue:
			if xxfirst_match == 0:
				pcm.detector('D3').hit(time, xxemission_time)

			if xxfirst_match == 1:
				pcm.detector('D4').hit(time, xxemission_time)

			if xxfirst_match == 2:
				pcm.detector('D3').hit(time, xxemission_time)

			if xxfirst_match == 3:
				pcm.detector('D4').hit(time, xxemission_time)	

		if xtrue:
			
			if xfirst_match == 0:
				pcm.detector('D1').hit(time, xemission_time)

			if xfirst_match == 1:
				pcm.detector('D1').hit(time, xemission_time)

			if xfirst_match == 2:
				pcm.detector('D2').hit(time, xemission_time)

			if xfirst_match == 3:
				pcm.detector('D2').hit(time, xemission_time)

		

			# Secondary emission

			# time_2 = time + xemission_time
			# xlifetime, xxlifetime = qd.generate_lifetimes()
			# poptime = qd.poptime()

			# if not constants.poptime_on:
			# 	poptime = 0

			# xtrue = np.random.random_sample() < constants.secondary_emission_probability*qd.x_probability(laser.power)

			
			# if xtrue:
	
			# 	state = qd.generate_state()
			# 	propogated_state = bench.matrix*state

			# 	D1D3_prob = pcm.channel('D1D3').calculate_probability(propogated_state)
			# 	D1D4_prob = pcm.channel('D1D4').calculate_probability(propogated_state)
			# 	D2D3_prob = pcm.channel('D2D3').calculate_probability(propogated_state)
			# 	D2D4_prob = pcm.channel('D2D4').calculate_probability(propogated_state)

			# 	prob = np.array([D1D3_prob, D1D4_prob, D2D3_prob, D2D4_prob])
			# 	boole = (prob.cumsum() > np.random.random_sample() )
			# 	first_match = np.where(boole ==True)[0][0] 				

			# 	if first_match == 0:
			# 		pcm.detector('D1').hit(time, xemission_time)

			# 	if first_match == 1:
			# 		pcm.detector('D1').hit(time, xemission_time)

			# 	if first_match == 2:
			# 		pcm.detector('D2').hit(time, xemission_time)

			# 	if first_match == 3:
			# 		pcm.detector('D2').hit(time, xemission_time)

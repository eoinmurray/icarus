


import numpy as np



def basis(qd, pcm, laser, bench, spectrometer, constants):
	"""
		Polarisation dependant cross corrolation experiment algorithm.
	"""

	for time in laser.pulseTimes(constants.integration_time):

		if np.random.random_sample() < constants.background_light_rate:
			
			bg_emission_time = np.random.choice(np.linspace(10., laser.pulse_width), 1)
			
			boole = ( (np.ones(4) * 0.25 ).cumsum() > np.random.random_sample() )
			first_match = np.where(boole == True)[0][0] 

			if first_match == 0:
				pcm.detector('D3').hit(time, bg_emission_time)

			if first_match == 1:
				pcm.detector('D4').hit(time, bg_emission_time)

			if first_match == 2:
				pcm.detector('D3').hit(time, bg_emission_time)

			if first_match == 3:
				pcm.detector('D4').hit(time, bg_emission_time)



		
		xxtrue, xtrue = qd.emission(laser.power) 
		xlifetime, xxlifetime = qd.generate_lifetimes()
		poptime = qd.poptime()
		
		if not constants.poptime_on:
			poptime = 0
		
		state = qd.generate_state()
		propogated_state = bench.matrix*state

		D1D3_prob = pcm.channel('D1D3').calculate_probability(propogated_state)
		D1D4_prob = pcm.channel('D1D4').calculate_probability(propogated_state)
		D2D3_prob = pcm.channel('D2D3').calculate_probability(propogated_state)
		D2D4_prob = pcm.channel('D2D4').calculate_probability(propogated_state)

		prob = np.array([D1D3_prob, D1D4_prob, D2D3_prob, D2D4_prob])
		boole = (prob.cumsum() > np.random.random_sample() )
		first_match = np.where(boole ==True)[0][0] 

		if xxtrue:
			if first_match == 0:
				pcm.detector('D3').hit(time, xxlifetime + poptime)

			if first_match == 1:
				pcm.detector('D4').hit(time, xxlifetime + poptime)

			if first_match == 2:
				pcm.detector('D3').hit(time, xxlifetime + poptime)

			if first_match == 3:
				pcm.detector('D4').hit(time, xxlifetime + poptime)	

		if xtrue:
			if first_match == 0:
				pcm.detector('D1').hit(time, xlifetime + poptime)

			if first_match == 1:
				pcm.detector('D1').hit(time, xlifetime + poptime)

			if first_match == 2:
				pcm.detector('D2').hit(time, xlifetime + poptime)

			if first_match == 3:
				pcm.detector('D2').hit(time, xlifetime + poptime)

		
			time_2 = time + xlifetime + poptime
			xlifetime, xxlifetime = qd.generate_lifetimes()
			poptime = qd.poptime()

			if not constants.poptime_on:
				poptime = 0

			xtrue = np.random.random_sample() < constants.secondary_emission_probability*qd.x_probability(laser.power)

			
			if xtrue:
	
				state = qd.generate_state()
				propogated_state = bench.matrix*state

				D1D3_prob = pcm.channel('D1D3').calculate_probability(propogated_state)
				D1D4_prob = pcm.channel('D1D4').calculate_probability(propogated_state)
				D2D3_prob = pcm.channel('D2D3').calculate_probability(propogated_state)
				D2D4_prob = pcm.channel('D2D4').calculate_probability(propogated_state)

				prob = np.array([D1D3_prob, D1D4_prob, D2D3_prob, D2D4_prob])
				boole = (prob.cumsum() > np.random.random_sample() )
				first_match = np.where(boole ==True)[0][0] 				

				if first_match == 0:
					pcm.detector('D1').hit(time, xlifetime + poptime)

				if first_match == 1:
					pcm.detector('D1').hit(time, xlifetime + poptime)

				if first_match == 2:
					pcm.detector('D2').hit(time, xlifetime + poptime)

				if first_match == 3:
					pcm.detector('D2').hit(time, xlifetime + poptime)

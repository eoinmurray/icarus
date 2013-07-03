import numpy as np
def basis(qd, pcm, laser, bench, spectrometer, constants):

	for time in laser.pulseTimes(constants.integration_time):

		xxtrue, xtrue = qd.emission(laser.power) # xxtrue is a biexciton photon, ie one photon not two, if xx is true x will also be true.
		xlifetime, xxlifetime = qd.lifetimes()
		poptime = np.random.exponential( constants.ptau - constants.xtau, size=1)[0]
		
		state = qd.generate_state()
		propogated_state = bench.matrix*state

		D1D3_prob = pcm.channel('D1D3').calculate_probability(propogated_state)
		D1D4_prob = pcm.channel('D1D4').calculate_probability(propogated_state)
		D2D3_prob = pcm.channel('D2D3').calculate_probability(propogated_state)
		D2D4_prob = pcm.channel('D2D4').calculate_probability(propogated_state)

		rand = np.random.random_sample()

		if xxtrue:
			if (0 < rand < D1D3_prob):
				pcm.detector('D3').hit(time, xxlifetime + poptime)

			elif (D1D3_prob < rand < D1D3_prob + D1D4_prob):
				pcm.detector('D4').hit(time, xxlifetime + poptime)

			elif (D1D3_prob + D1D4_prob < rand < D1D3_prob + D1D4_prob + D2D3_prob):
				pcm.detector('D3').hit(time, xxlifetime + poptime)

			if (D1D3_prob + D1D4_prob + D2D3_prob < rand < D1D3_prob + D1D4_prob + D2D3_prob + D2D4_prob):
				pcm.detector('D4').hit(time, xxlifetime + poptime)	

		if xtrue:
			if (0 < rand < D1D3_prob):
				pcm.detector('D1').hit(time, xlifetime + poptime)

			if (D1D3_prob < rand < D1D3_prob + D1D4_prob):
				pcm.detector('D1').hit(time, xlifetime + poptime)

			if (D1D3_prob + D1D4_prob < rand < D1D3_prob + D1D4_prob + D2D3_prob):
				pcm.detector('D2').hit(time, xlifetime + poptime)

			if (D1D3_prob + D1D4_prob + D2D3_prob < rand < D1D3_prob + D1D4_prob + D2D3_prob + D2D4_prob):
				pcm.detector('D2').hit(time, xlifetime + poptime)

			if constants.secondary_emission:
			
				time_2 = time + xlifetime + poptime
				xlifetime, xxlifetime = qd.lifetimes()
				poptime = np.random.exponential( constants.ptau - constants.xtau, size=1)[0]
			
				xtrue = np.random.random_sample() < constants.secondary_emission_probability*qd.x_probability(laser.power**constants.secondary_emission_degree)
				
				if xtrue:
					if np.random.random_sample() < 0.5:
						pcm.detector('D2').hit(time_2, xlifetime + poptime)
					else:
						pcm.detector('D1').hit(time_2, xlifetime + poptime)
import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

from scipy import integrate, interpolate, optimize
import numpy as np
import matplotlib.pyplot as plt
import constants as constants
from Experiment import Experiment


def function(secondary_emission_probability):
	constants.secondary_emission_probability = secondary_emission_probability
	experiment = Experiment(constants, Visualizer=False)
	experiment.run('auto')

	x_gen = experiment.pcm.channel('D1D3').bin_edges
	y_gen = experiment.pcm.channel('D1D3').counts

	return x_gen, y_gen


if __name__ == "__main__":
		

	range_lower = 0
	range_upper = 400
	ZeroPoint 	= 0
	range = np.array([range_lower, range_upper])
	x_data, y_data = model.get('pulsed.dat', ZeroPoint, [range_lower, range_upper])

	peak_place_width = constants.pulse_width
	hold_int = []
	hold_max = []
	
	# process the peaks
	for i in xrange(int(x_data.max()/peak_place_width)):
		minIdx = np.abs(x_data - peak_place_width*i).argmin()
		maxIdx = np.abs(x_data - peak_place_width*(i+1)).argmin()
		peakX = x_data[minIdx: maxIdx]
		peakY = y_data[minIdx:maxIdx]	
		
		if i != 6:
			hold_max.append( np.max(peakY) )
			hold_int.append( np.sum(peakY) )
		else:
			delay_peak = np.sum(peakY)

	# normalise
	y_data = y_data/np.mean(hold_max)
	print delay_peak/np.mean(hold_int)
	x_data = x_data[0:x_data.size - 1]
	y_data = y_data[0:y_data.size - 1]
	
	plt.plot(x_data, y_data)
	plt.show()
	
	initial_guess = np.linspace(0, 0.4, num=10)
	hold_residuals_squared 	= np.zeros(initial_guess.size)

	for i in xrange(initial_guess.size):
		
		x_gen, y_gen = function( initial_guess[i] )
		hold_int = []
		hold_max = []
		
		for j in xrange(int(x_gen.max()/peak_place_width)):
			minIdx = np.abs(x_gen - peak_place_width*j).argmin()
			maxIdx = np.abs(x_gen - peak_place_width*(j+1)).argmin()
			peakX = x_gen[minIdx: maxIdx]
			peakY = y_gen[minIdx:maxIdx]	
			
			if j != 6:
				hold_max.append( np.max(peakY) )
				hold_int.append( np.sum(peakY) )
			else:
				delay_peak = np.sum(peakY)

		y_gen = y_gen/np.mean(hold_max)
		print delay_peak/np.mean(hold_int)
		
		residuals = (y_data - y_gen)
		hold_residuals_squared[i] = (residuals**2).sum()

	print hold_residuals_squared
	
	min_residual_idx = hold_residuals_squared.argmin()
	c = initial_guess[min_residual_idx]
	print hold_residuals_squared	
	print "guesses were         ", initial_guess
	print "best fit is ", c
	
	c = 0.20
	x_gen, y_gen = function( c )	
	hold_int = []
	hold_max = []
	
	for i in xrange(int(x_gen.max()/peak_place_width)):
		minIdx = np.abs(x_gen - peak_place_width*i).argmin()
		maxIdx = np.abs(x_gen - peak_place_width*(i+1)).argmin()
		peakX = x_gen[minIdx: maxIdx]
		peakY = y_gen[minIdx:maxIdx]	
		
		if i != 6:
			hold_max.append( np.max(peakY) )
			hold_int.append( np.sum(peakY) )
		else:
			delay_peak = np.sum(peakY)

	y_gen = y_gen/np.mean(hold_max)
	print delay_peak/np.mean(hold_int)
	plt.plot(x_data, y_data, 'r--')
	plt.plot(x_gen, y_gen, 'b-')
	plt.ylabel('counts')
	plt.xlabel('time')
	plt.legend(('data', 'simulated'), loc=0)	
	plt.show()









import os,sys ; parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) ; sys.path.insert(0,parentdir)
import numpy as np 
import matplotlib.pyplot as plt
from Icarus.Classes.QuantumDot import QuantumDot
from constants import Constants
np.set_printoptions(precision=3)



class NormalizationError(Exception):
	pass



def lifetime_and_phase(qd):
	"""
		Generates a lifetime and then phase, returns phase.
	"""

	qd.generate_lifetimes()
	return qd.generate_phase()


	
def phase_normalized(constants):
	"""
		Makes sure that the phases are normalized
	"""
	
	qd = QuantumDot(constants.xtau, constants.xxtau, constants.ptau, constants.FSS, constants.crosstau)
	
	phases = np.array([lifetime_and_phase(qd) for i in xrange(10000)])
	is_normalized = (np.around(np.abs(phases), decimals=4) == 1)
	num_fails =  is_normalized[is_normalized == False].size

	if num_fails > 0:

		print phases[is_normalized == False]
		raise TestErrors.NormalizationError('Not all the phases are normalized to 1, ', num_fails, 'failed.')

	else:
	
		return 1



def plot_phase_distributions(constants):
	"""
		Plot the distribution of phases.
	"""

	qd = QuantumDot(constants.xtau, constants.xxtau, constants.ptau, constants.FSS, constants.crosstau)
	
	phases = np.array([lifetime_and_phase(qd) for i in xrange(10000)])

	counts, bin_edges = np.histogram(phases, np.linspace(0, 1, 101))

	fig = plt.figure()
	ax = fig.add_subplot(111)
	rects1 = ax.bar(bin_edges[0: counts.size], counts, 0.01, color='r')

	plt.xlim([0, 1])

	plt.show()



def plot_fidelity_lorentzian(constants):
	"""
		Plots the Fidelity vs FSS curve with and without decoherence.
	"""

	qd = QuantumDot(constants.xtau, constants.xxtau, constants.ptau, constants.FSS, constants.crosstau)

	fss = np.linspace(-10., 10., 500)*1e-6
	no_decoherence = np.array([qd.ideal_fidelity_lorentzian(f, constants.xtau, 0)[0] for f in fss])
	with_decoherence = np.array([qd.ideal_fidelity_lorentzian(f, constants.xtau, constants.crosstau)[0] for f in fss])

	fss = fss/1e-6
	decoherence = qd.ideal_fidelity_lorentzian(f, constants.xtau, constants.crosstau)[1]

	plt.figure(figsize = (16./1.3, 9./1.3))
	plt.plot(fss, no_decoherence, 'r--', fss, with_decoherence, 'b--')

	plt.xlim([-10, 10]) ; plt.ylim([0.45, 1])
	plt.xlabel('Fine structure splitting $eV$') ; plt.ylabel('Fidelity')
	plt.legend(['No decoherence', 'With $1^{st}$ coherence: ' + np.array(decoherence).astype('|S3').tostring()])
	plt.show()


if __name__ == "__main__":
	constants = Constants()
	# if phase_normalized(constants): print 'phase_normalized() test passed.'
	plot_fidelity_lorentzian(constants)
	# plot_phase_distributions(constants)
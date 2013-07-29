


import os,sys ; parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) ; sys.path.insert(0,parentdir)
import numpy as np 
from Icarus.Classes.QuantumDot import QuantumDot



class NormalizationError(Exception):
	pass



def lifetime_and_phase(qd):
	"""
		Generates a lifetime and then phase, returns phase.
	"""

	qd.generate_lifetimes()
	return qd.generate_phase()


	
def phase_normalized():
	"""
		Makes sure that the phases are normalized
	"""
	
	qd = QuantumDot(1, 0.5, 0.2, 0, 2.5)
	
	phases = np.array([lifetime_and_phase(qd) for i in xrange(10000)])
	is_normalized = (np.around(np.abs(phases), decimals=4) == 1)
	num_fails =  is_normalized[is_normalized == False].size

	if num_fails > 0:

		print phases[is_normalized == False]
		raise TestErrors.NormalizationError('Not all the phases are normalized to 1, ', num_fails, 'failed.')

	else:
	
		return 1



if __name__ == "__main__":

	if phase_normalized(): print 'phase_normalized() test passed.'
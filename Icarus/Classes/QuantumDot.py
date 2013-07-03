import numpy as np

class QuantumDot:
	def __init__(self, xlifetime=None, xxlifetime=None, FSS=None):
		self.initializeMatrices()
		self.xtau = xlifetime
		self.xxtau = xxlifetime
		
		self.FSS = FSS

		self.xlifetime = 0
		self.xxlifetime = 0
		self.temp_hold_xlifetime = 10000
		self.phase = 0

	def initializeMatrices(self):
		self.i = np.matrix([[1],[0]])
		self.j = np.matrix([[0],[1]])
		self.h = np.matrix([[1],[0]])
		self.v = np.matrix([[0],[1]])
		self.x = np.matrix([[1],[0]])
		self.xx = np.matrix([[0],[1]])

		self.ixh = np.kron(self.x, np.kron(self.i, self.h))
		self.jxh = np.kron(self.x, np.kron(self.j, self.h))
		self.ixv = np.kron(self.x, np.kron(self.i, self.v))
		self.jxv = np.kron(self.x, np.kron(self.j, self.v))

		self.ixxh = np.kron(self.xx, np.kron(self.i, self.h))
		self.jxxh = np.kron(self.xx, np.kron(self.j, self.h))
		self.ixxv = np.kron(self.xx, np.kron(self.i, self.v))
		self.jxxv = np.kron(self.xx, np.kron(self.j, self.v))

	def lifetimes(self):
		xlifetime = 1
		xxlifetime = 10
		while xlifetime < xxlifetime:
			xlifetime = np.random.exponential( self.xtau, 1)[0]
			xxlifetime = np.random.exponential( self.xxtau, 1)[0]
		self.xlifetime = xlifetime
		self.xxlifetime = xxlifetime
		return xlifetime, xxlifetime

	def generate_phase(self):
		hbar = 6.56e-16
		if self.temp_hold_xlifetime == self.xlifetime:
			print '[Warning] Using the same lifetime twice in a row to generate the state phase, are you sure this is correct? '
			print 'Normally you should generate a new lifetime each iteration of the experiment.'
		phase = np.exp((1.0j*self.FSS*self.xlifetime*1E-9)/hbar)
		self.temp_hold_xlifetime = self.xlifetime
		self.phase = phase
		return phase

	def generate_state(self):
		self.generate_phase()
		state = (1.0/np.sqrt(2.0))*( np.kron(self.ixh, self.ixxh) + self.phase*np.kron(self.ixv,self.ixxv))
		self.state = state
		return state

	def x_probability(self, power):
		return 1 - np.exp(- power)
	
	def xx_probability(self, power):		
		return 1 - (1+ power)*np.exp(- power)

	def x_emission(self, power):
		boole = (np.random.random_sample() < self.x_probability(power)) 
		return boole

	def xx_emission(self, power):
		boole = (np.random.random_sample() < self.xx_probability(power)) 
		return boole

	def emission(self, power):
		if self.xx_emission(power):
			return True, True

		elif self.x_emission(power):
			return False, True
			
		else:
			return False, False

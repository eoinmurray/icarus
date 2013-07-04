

import numpy as np

class QuantumDot:
	def __init__(self, xlifetime=None, xxlifetime=None, ptau = None, FSS=None):
		self.initializeMatrices()
		self.xtau = xlifetime
		self.xxtau = xxlifetime
		self.ptau = ptau
		
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

	def poptime(self):
		return np.random.exponential( self.ptau - self.xtau, size=1)[0]

	def generate_phase(self):
		hbar = 6.56e-16
		self.phase = self._generate_phase(self.FSS, self.xlifetime, hbar)
		return self.phase

	def _generate_phase(self, FSS, xlifetime, hbar):
		return np.exp((1.0j*FSS*xlifetime*1e-9)/hbar)

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




import numpy as np



class RepeatLifetimes(Exception):
    pass



class UnsetLifetimes(Exception):
	pass



class NormalizationError(Exception):
	pass



# _function denotes a local only function, it should not be used outside this file.



class QuantumDot:
	"""	
		Handles the generation of lifetimes, quantum state, state phase, state matrix 
		and probability of emission.
	"""
	

	def __init__(self, xtau=None, xxtau=None, ptau=None, FSS=None, crosstau=None):
		"""
			Initialize.
		"""

		self.initializeMatrices()
		self.xtau = xtau

		self.xxtau = xxtau
		self.ptau = ptau
		self.crosstau = crosstau
		
		self.FSS = FSS

		self.xlifetime = 0
		self.xxlifetime = 0
		self.xlifetime_last = 1
		self.xxlifetime_last = 1
		self.temp_hold_xlifetime = 10000
		self.phase = 0

		self.choice_array = np.linspace(-1., 1., 2000)

	

	def initializeMatrices(self):
		"""
			Initialize the matrices.
		"""

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

	

	def generate_lifetimes(self):
		"""
			Generates lifetimes, the biexciton lifetime is always shorter than the exciton.
		"""

		xlifetime = np.random.exponential( self.xtau, 1)[0]
		xxlifetime = np.random.exponential( self.xxtau, 1)[0]
	
		while xxlifetime > xlifetime:
			xxlifetime = np.random.exponential( self.xxtau, 1)[0]

		self.xlifetime_last = self.xlifetime
		self.xxlifetime_last = self.xxlifetime
	
		self.xlifetime = xlifetime
		self.xxlifetime = xxlifetime
		return xlifetime, xxlifetime

	

	def poptime(self):
		"""
			Calculates a population time for an exciton coming in from the wires/bulk.
		"""

		return np.random.exponential( self.ptau - self.xtau, size=1)[0]



	def check_lifetimes(self):
		"""
			Checks if xlifetime_last is not the same as xlifetime current.
		"""

		if self.xlifetime == self.xlifetime_last:
			raise Errors.RepeatLifetimes('Lifetimes are being reused. Use QuantumDot.lifetimes() to generate lifetimes.')

		if self.xlifetime == 0:
			raise Errors.UnsetLifetimes('Lifetimes have not been set. Use QuantumDot.lifetimes() to generate lifetimes.')			



	def ideal_fidelity_lorentzian(self, fss = None):
		"""
			Returns ideal fidelty, from AH thesis pg 72.
			Slightly simplified with k = ghv' = 1.
		"""

		xtau = self.xtau*1e-9
		if fss == None:
			fss = self.FSS
		crosstau = self.crosstau*1e-9

		hbar = 6.56e-16 # eV

		if crosstau == 0.0: 
			ghv = 1.0
		else:
			ghv = 1/(1 + xtau/crosstau)

		x = ghv*fss*xtau/hbar

		return 0.25 * (2 + 2*ghv / (1 + x**2)), ghv

	

	def generate_state(self):
		"""
			Calculates a state based on the phase and polarization.
		"""

		self.generate_phase()
		state = (1.0/np.sqrt(2.0))*( np.kron(self.ixh, self.ixxh) + self.phase*np.kron(self.ixv,self.ixxv))
		self.state = state
		return state
	


	def generate_phase(self):
		"""
			Calculates a phase based on the FSS.
		"""

		self.check_lifetimes()

		self.phase = self.generate_fss_phase()
		dephase = self.generate_cross_dephasing()
		
		# if dephase != None:
		# 	self.phase += dephase

		self.phase = self.phase/np.abs(self.phase)
		return self.phase

	

	def generate_fss_phase(self):
		"""
			The actual expression for the phase, only exists as a seperate function for testing.			
		"""

		hbar = 6.56e-16 # eV
		return np.exp((1.0j*self.FSS*self.xlifetime*1e-9)/hbar)



	def generate_cross_dephasing(self):
		"""
			Implements critical result of pure dephasing.
		"""

		self.check_lifetimes()
		ghv = self.ideal_fidelity_lorentzian()[1]

		if (ghv > 1.0) or (ghv < 0.0): 
			raise ValueError('First order coherence is greater than one.')

		if float(self.crosstau) == 0.0: 
			return None

		elif np.random.random_sample() > ghv:
			c = np.random.choice(self.choice_array) + np.random.choice(self.choice_array) * 1j
			cp = (c/np.abs(c))*0.01

			# if np.around(np.abs(cp), decimals=2) != 1.0:
				# raise NormalizationError('New cross dephasing phase is not normalized.', np.abs(cp))

			return cp
		
		else:
			return None



	def x_probability(self, power):
		"""
			X probability based on power.
		"""

		return 1 - np.exp(- power)
	
	

	def xx_probability(self, power):		
		"""
			XX probability based on power.
		"""

		return 1 - (1+ power)*np.exp(- power)

	

	def x_emission(self, power):
		"""
			X emission based on X probability.
		"""

		boole = (np.random.random_sample() < self.x_probability(power)) 
		return boole

	

	def xx_emission(self, power):
		"""
			XX emission based on XX probability.
		"""

		boole = (np.random.random_sample() < self.xx_probability(power)) 
		return boole

	

	def emission(self, power):
		"""
			Return two booles whether XX and X, only X or no emission occurs.
		"""

		if self.xx_emission(power):
			return True, True

		elif self.x_emission(power):
			return False, True
			
		else:
			return False, False

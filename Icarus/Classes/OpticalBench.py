

import numpy as np
from Laser import Laser

class OpticalBench:

	def __init__(self):
		self.Laser = Laser
		self.initializeJonesMatrices()

	def setHWP(self, t1 ,t2):
		self.HWP = self.calculate_HWP(t1, t2)
		self.HWPHWP = np.kron(self.HWP, self.HWP)

	def setQWP(self, t1 ,t2):
		self.QWP = self.calculate_QWP(t1, t2)
		self.QWPQWP = np.kron(self.QWP, self.QWP)

	def getHWP(self):
		return self.HWP

	def getQWP(self):
		return self.QWP

	def getHWPHWP(self):
		return self.HWPHWP

	def getQWPQWP(self):
		return self.QWPQWP

	def setLabMatrix(self, element_names):
		element_names = element_names.split(' ')

		isSet = False
		for element_name in element_names:
			el = getattr(self, element_name)
			if not isSet:
				temp = el
				isSet = True
			else:
				temp = el*temp

		self.labMatrix = temp
		self.matrix = temp

	def getLabMatrix(self):
		return self.labMatrix

	def initializeJonesMatrices(self):
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

		self.PBS = np.matrix([
			[1, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 1, 0, 0, 0, 0],
			[0, 0, 1, 0, 0, 0, 0, 0],
			[0, 1, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 1, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 1],
			[0, 0, 0, 0, 0, 0, 1, 0],
			[0, 0, 0, 0, 0, 1, 0, 0]
		])

		self.S = np.matrix([
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 1, 0, 0, 0, 0, 0],
			[0, 0, 0, 1, 0, 0, 0, 0],
			[0, 0, 0, 0, 1, 0, 0, 0],
			[0, 0, 0, 0, 0, 1, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0]
		])

		self.NBS = (1/np.sqrt(2))*np.matrix([
			[1, 0, 1, 0, 0, 0, 0, 0],
			[0, 1, 0, 1, 0, 0, 0, 0],
			[1, 0, 1, 0, 0, 0, 0, 0],
			[0, 1, 0, 1, 0, 0, 0, 0],
			[0, 0, 0, 0, 1, 0, 1, 0],
			[0, 0, 0, 0, 0, 1, 0, 1],
			[0, 0, 0, 0, 1, 0, 1, 0],
			[0, 0, 0, 0, 0, 1, 0, 1]
		])

		# The two particle state elements. 
		self.PBSPBS = np.kron(self.PBS, self.PBS)
		self.SS = np.kron(self.S, self.S)
		self.NBSNBS = np.kron(self.NBS, self.NBS)

	def calculate_HWP(self, t1, t2):
		return np.matrix([
			[np.cos(t1)**2 - np.sin(t1)**2, 2*np.cos(t1)*np.sin(t1), 0, 0, 0, 0, 0, 0],
			[2*np.cos(t1)*np.sin(t1), -np.cos(t1)**2 + np.sin(t1)**2, 0, 0, 0, 0, 0, 0],
			[0, 0, np.cos(t1)**2 - np.sin(t1)**2, 2*np.cos(t1)*np.sin(t1), 0, 0, 0, 0],
			[0, 0, 2*np.cos(t1)*np.sin(t1), -np.cos(t1)**2 + np.sin(t1)**2, 0, 0, 0, 0],
			[0, 0, 0, 0, np.cos(t2)**2 - np.sin(t2)**2, 2*np.cos(t2)*np.sin(t2), 0, 0],
			[0, 0, 0, 0, 2*np.cos(t2)*np.sin(t2), -np.cos(t2)**2 + np.sin(t2)**2, 0, 0],
			[0, 0, 0, 0, 0, 0, np.cos(t1)**2 - np.sin(t1)**2, 2*np.cos(t1)*np.sin(t1)],
			[0, 0, 0, 0, 0, 0, 2*np.cos(t1)*np.sin(t1), -np.cos(t1)**2 + np.sin(t1)**2]
		])

	def calculate_QWP(self, t1, t2):
		return np.matrix([
			[np.cos(t1)**2 + 1j*np.sin(t1)**2, (1-1j)*np.cos(t1)*np.sin(t1), 0, 0, 0, 0, 0, 0],
			[(1-1j)*np.cos(t1)*np.sin(t1), 1j*np.cos(t1)**2 + np.sin(t1)**2, 0, 0, 0, 0, 0, 0],
			[0, 0, np.cos(t1)**2 + 1j*np.sin(t1)**2, (1-1j)*np.cos(t1)*np.sin(t1), 0, 0, 0, 0],
			[0, 0, (1-1j)*np.cos(t1)*np.sin(t1), 1j*np.cos(t1)**2 + np.sin(t1)**2, 0, 0, 0, 0],
			[0, 0, 0, 0, np.cos(t2)**2 + 1j*np.sin(t2)**2, (1-1j)*np.cos(t2)*np.sin(t2), 0, 0],
			[0, 0, 0, 0, (1-1j)*np.cos(t2)*np.sin(t2), 1j*np.cos(t2)**2 + np.sin(t2)**2, 0, 0],
			[0, 0, 0, 0, 0, 0, np.cos(t2)**2 + 1j*np.sin(t2)**2, (1-1j)*np.cos(t2)*np.sin(t2)],
			[0, 0, 0, 0, 0, 0, (1-1j)*np.cos(t2)*np.sin(t2), 1j*np.cos(t2)**2 + np.sin(t2)**2],
		])





import numpy as np
from Channel import Channel
from Detector import Detector



class PhotonCountingModule():
	"""
		Handles the registration of detectors and channels.
		Detector and Channel class should only be used through this.
	"""



	def __init__(self):
		"""
			Initialize.
		"""

		self.Detector = Detector
		self.Channel = Channel

		self._detectors = {}
		self._channels = {}



	def register_detector(self, name, detector):
		"""
			Registers a named detector if not already in use.
		"""

		if name in self._detectors:
			raise NameError('Detector name:['+name+'] is already in use.')
		else:
			self._detectors[name] = detector



	def register_channel(self, name, channel):
		"""
			Registers a named channel if not already in use.
		"""

		if name in self._channels:
			raise NameError('Channel name:['+name+'] is already in use.')
		else:
			self._channels[name] = channel



	def detector(self, name):
		"""
			return a named detector.
		"""

		return self._detectors[name]



	def channel(self, name):
		"""
			return a named channel.
		"""

		return self._channels[name]
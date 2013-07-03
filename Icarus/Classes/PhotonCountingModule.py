import numpy as np
from Channel import Channel
from Detector import Detector


class PhotonCountingModule():

	def __init__(self):
		self.Detector = Detector
		self.Channel = Channel

		self._detectors = {}
		self._channels = {}

	def register_detector(self, name, detector):
		if name in self._detectors:
			raise NameError('Detector name:['+name+'] is already in use.')
		else:
			self._detectors[name] = detector

	def register_channel(self, name, channel):
		if name in self._channels:
			raise NameError('Channel name:['+name+'] is already in use.')
		else:
			self._channels[name] = channel

	def detector(self, name):
		return self._detectors[name]

	def channel(self, name):
		return self._channels[name]
import numpy as np
from Classes.PhotonCountingModule import PhotonCountingModule
from Classes.QuantumDot import QuantumDot
from Classes.OpticalBench import OpticalBench
from Classes.Visualizer import Visualizer
from Classes.EventEmitter import EventEmitter
from Classes.Spectrometer import Spectrometer

class Icarus(EventEmitter):
	def __init__(self):
		self.QuantumDot = QuantumDot
		self.PhotonCountingModule = PhotonCountingModule
		self.OpticalBench = OpticalBench
		self.Visualizer = Visualizer
		self.Spectrometer = Spectrometer

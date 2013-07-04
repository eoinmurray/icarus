import matplotlib.pyplot as plt 
import numpy as np 

class Visualizer:
	def __init__(self):		
		self.plt = plt
		self.plt.ion()
		self.fig = self.plt.figure()
		self._channels = {}
		self._plots = {}

	def add(self, channel, pos):
		self._channels[channel.name] = channel
		ax = self.fig.add_subplot(pos, xlim=(0,300), ylim=(0,10))
		ax.set_xlabel(channel.name)
		line, = ax.plot(channel.bin_edges, channel.counts, 'r-')
		self._plots[channel.name] = {'ax' : ax, 'line' : line}

	def update(self, name):
		channel = self._channels[name]
		self._plots[name]['ax'].set_ylim([0, np.max(channel.counts) + 5])
		self._plots[name]['line'].set_ydata(channel.counts)
		self.fig.canvas.draw()

	def bind(self, name):
		def echo(obj):
			self.update(name)
		self._channels[name].on('change', echo)

	def plot(self, channel, pos):
		self._channels[channel.name] = channel
		ax = self.fig.add_subplot(pos, xlim=(0,300))
		ax.set_xlabel(channel.name)
		ax.plot(channel.bin_edges, channel.counts, 'r-')
		# ax.set_ylim([0, np.max(channel.counts) + 5])
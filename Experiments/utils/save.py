

import os,sys
import datetime
import numpy as np 
import matplotlib.pyplot as plt

today = datetime.datetime.now().strftime("%Y-%m-%d")
directory = os.path.dirname("out/" + today + '/')

try:
	os.mkdir('out/')
except OSError:
	pass

try:
	os.mkdir(directory)
except OSError:
	pass


def savefig(plt, name = None, dir = None):
	if not name:
		raise NameError('You need to specify a filename.')

	filename = directory + '/' + name + '.png'
	
	if dir:
		try:
			os.mkdir(directory + '/' + dir)
		except OSError:
			pass		
		filename = directory + '/' + dir + '/' + name + '.png'

	plt.savefig(filename)
	plt.close('all')


def savedata(x, y, name = None, dir = None):
	if not name:
		raise NameError('You need to specify a filename.')

	filename = directory + '/' + name + '.txt'
	data = np.vstack((x,y)).T

	if dir:
		try:
			os.mkdir(directory + '/' + dir)
		except OSError:
			pass		
		
		filename = directory + '/' + dir + '/' + name + '.txt'
	
	np.savetxt(filename, data, delimiter = ',')

def plotdata(name, dir):
	filename = directory + '/' + dir + '/' + name
	data =  np.loadtxt(filename + ' D1D3.txt', delimiter = ',')	
	x = data[:,0]
	y1 = data[:,1]
	data = np.loadtxt(filename + ' D1D4.txt', delimiter = ',')	
	y2 = data[:,1]
	data = np.loadtxt(filename + ' D2D3.txt', delimiter = ',')	
	y3 = data[:,1]
	data = np.loadtxt(filename + ' D2D4.txt', delimiter = ',')	
	y4 = data[:,1]

	ymax = np.array([y1, y2, y3, y4]).max() + 2

	plt.suptitle(name)

	plt.subplot(221)
	plt.plot(x, y1) 
	plt.xlim([0,300]) 
	plt.ylim([0, ymax + 2])
	plt.ylabel('Counts')
	plt.xlabel('Time (ns)')
	plt.annotate('D1D3', xy=(0, 1), xytext=(12, -12), va='top', xycoords='axes fraction', textcoords='offset points')

	plt.subplot(222)
	plt.plot(x, y2)
	plt.xlim([0,300]) 
	plt.ylim([0, ymax + 2])	
	plt.ylabel('Counts')
	plt.xlabel('Time (ns)')
	plt.annotate('D1D4', xy=(0, 1), xytext=(12, -12), va='top', xycoords='axes fraction', textcoords='offset points')	

	plt.subplot(223)
	plt.plot(x, y3)
	plt.xlim([0,300]) 
	plt.ylim([0, ymax + 2])
	plt.ylabel('Counts')
	plt.xlabel('Time (ns)')
	plt.annotate('D2D3', xy=(0, 1), xytext=(12, -12), va='top', xycoords='axes fraction', textcoords='offset points')

	plt.subplot(224)
	plt.plot(x, y4)
	plt.xlim([0,300]) 
	plt.ylim([0, ymax + 2])
	plt.ylabel('Counts')
	plt.xlabel('Time (ns)')
	plt.annotate('D2D4', xy=(0, 1), xytext=(12, -12), va='top', xycoords='axes fraction', textcoords='offset points')	
	
	return plt


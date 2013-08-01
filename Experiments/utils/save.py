


import os,sys
import datetime
import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import string
import random



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
	"""
		Saves a plot.
	"""

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



def random_dirname():
	"""
		Returns a random dirname
	"""

	return ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(5))



def savedata(x, y, name = None, dir = None):
	"""
		Saves data.
	"""

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



def save_params(dir):
	"""
		Saves constants.py to a text file
	"""

	from constants import Constants
	constants = Constants()
	import inspect
	param_string = ''.join(inspect.getsourcelines(Constants)[0])

	try:
		os.mkdir(directory + '/' + dir)
	except OSError:
		pass		

	with open(directory + '/' + dir + "/params.txt", "w") as text_file:
		text_file.write(param_string)



def plotdata(name, dir):
	"""
		Plots saves data.
	"""

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



def plot_matrix(matrix, title):
	"""
		3D bar chart of density matrix.
	"""

	
	data = np.squeeze(np.asarray(matrix))
	
	column_names = ['HH', 'HV', 'VH', 'VV']
	row_names = ['HH', 'HV', 'VH', 'VV']

	fig = plt.figure()
	ax = Axes3D(fig)

	lx= len(data[0])            # Work out matrix dimensions
	ly= len(data[:,0])

	xpos = np.arange(0,lx,1)    # Set up a mesh of positions
	ypos = np.arange(0,ly,1)
	xpos, ypos = np.meshgrid(xpos + 0.25, ypos + 0.25)

	xpos = xpos.flatten()   # Convert positions to 1D array
	ypos = ypos.flatten()
	zpos = np.zeros(lx*ly)

	dx = 0.5 * np.ones_like(zpos)
	dy = dx.copy()
	dz = data.flatten()

	ax.bar3d(xpos,ypos,zpos, dx, dy, dz, color='b')
	
	ax.w_xaxis.set_ticks([0.5, 1.5, 2.5, 3.5])
	ax.w_yaxis.set_ticks([0.5, 1.5, 2.5, 3.5])
	ax.w_xaxis.set_ticklabels(column_names)
	ax.w_yaxis.set_ticklabels(row_names)
	ax.set_zlim([0,1])
	plt.suptitle(title)
	return plt

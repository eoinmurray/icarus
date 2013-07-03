import os,sys
import datetime
import numpy as np 

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
	
	np.savetxt(directory + '/' + name + '.txt', data, delimiter = ',')
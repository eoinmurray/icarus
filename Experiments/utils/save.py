import os,sys
import datetime

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

	if dir:
		try:
			os.mkdir(directory + '/' + dir)
		except OSError:
			pass		
		
		plt.savefig(directory + '/' + dir + '/' + name + '.png')
	
	else:
		plt.savefig(directory + '/' + name + '.png')
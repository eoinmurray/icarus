import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

import numpy as np
import matplotlib.pyplot as plt
import constants as constants
from Experiments import Experiment
import utils.save as save


experiment = Experiment(constants, Visualizer = True)

experiment.bench.setHWP(0, 0)
experiment.bench.setLabMatrix('NBSNBS HWPHWP SS PBSPBS')
	
experiment.run('basis')
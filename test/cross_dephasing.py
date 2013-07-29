


import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) ; sys.path.insert(0,parentdir)
import numpy as np 
from Icarus.Classes.QuantumDot import QuantumDot



if __name__ == "__main__":

	qd = QuantumDot(1, 0.5, 0.2, 0, 2.5)
	qd.generate_lifetimes()
	print qd.generate_phase()
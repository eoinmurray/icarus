# Icarus documentation.

## Constants
	
Class that holds the quantum dot and experiment parameters.

```python
	from constants import Constants
	constants = Constants()
```

## Icarus.QuantumDot

```python
	from Icarus import QuantumDot
	qd = QuantumDot(constants.xtau, constants.xxtau, constants.ptau, constants.FSS, constants.crosstau)
```

# Ipython notebooks

[Fidelity vs FSS](http://nbviewer.ipython.org/urls/raw.github.com/eoinmurray/icarus/master/Fidelity%2520verus%2520Fine%2520structure%2520splitting.ipynb)

[Pure dephasing monte carlo](http://nbviewer.ipython.org/urls/raw.github.com/eoinmurray/icarus/master/Pure%2520dephasing%2520monte%2520carlo.ipynb)
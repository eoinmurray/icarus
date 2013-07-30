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

#[Fidelity vs FSS notebook](http://nbviewer.ipython.org/urls/raw.github.com/eoinmurray/icarus/master/Fidelity%2520verus%2520Fine%2520structure%2520splitting.ipynb)
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

## Icarus.Detector

```python
	from Icarus import Detector
	detector = Detector(delay, efficiency, sigma, matrix)
```

## Icarus.Channel

```python
	from Icarus import Channel
	channel = Channel(bin_width, detector1, detector2, name)
```

## Icarus.PhotonCountingModule

```python
	from Icarus import PhotonCountingModule
	pcm = PhotonCountingModule()
	pcm.register_detector(name, detector)
	pcm.register_channel(name, channel)
```

## Icarus.Laser

```python
	from Icarus import Laser
	laser = Laser(pulse_width, power)
```

## Icarus.OpticalBench

```python
	from Icarus import OpticalBench
	opticalbench = OpticalBench()
```

## Icarus.Spectrometer

```python
	from Icarus import Spectrometer
	spectrometer = Spectrometer()
```

# Ipython notebooks

[Fidelity vs FSS](http://nbviewer.ipython.org/urls/raw.github.com/eoinmurray/icarus/master/Fidelity%2520verus%2520Fine%2520structure%2520splitting.ipynb)

[Pure dephasing monte carlo](http://nbviewer.ipython.org/urls/raw.github.com/eoinmurray/icarus/master/Pure%2520dephasing%2520monte%2520carlo.ipynb)
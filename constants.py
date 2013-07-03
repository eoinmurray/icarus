import numpy as np
# All times in nanoseconds
# In real experiment integration time is 0.5e9ns, but detector yield is also much much lower.

# Quantum dot
xtau = 1.7
xxtau = 0.9
ptau = 2.5
poptime = False
FSS = 0.4e-6
hbar = 6.58e-16
secondary_emission = True
secondary_emission_probability = 0.1
secondary_emission_degree = 1

# Laser
pulse_width = 25.
mean_photon_number = 0.8
power = mean_photon_number

# Detector
FWHM = 4.8
sigma = FWHM/(2*np.sqrt(np.log(2)*2))
# sigma = 0
efficiency = 1
delay = 161.8
gate_start = 0.5
gate_width = 1
time_gating = False
bin_width = 50

# Experiment parameters
num_iterations = 1000
integration_time = 4000
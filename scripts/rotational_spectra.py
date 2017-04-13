from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt

def read_energies():
    with open('../data/energy.dat', mode = 'r') as inputfile:
        lines = inputfile.readlines()

    J = []
    energies = []

    for line in lines:
        if 'J' in line:
            J.append(float(line.split()[-1]))
        if line.split()[0].isdigit():
            if int(line.split()[0]) == 0:
                energies.append(float(line.split()[1]))
    
    return energies, J

def model_spectra(temperature):
    transitions = []
    intensities = []

    for j, e1, e2 in zip(J, energies, energies[1:]):
        transitions.append(e2 - e1)
        intensities.append(d0**2 * (j + 1) * np.exp(- h * c * rotational_constant * j * (j + 1) / (k * temperature)))
    
    return transitions, intensities

# --------------------------
# CONSTANTS
h = 6.626070040*10**(-34) # J * s
k = 1.38064852 * 10**(-23) # J / K
da = 1.66053904 * 10**(-27) # da to kg
c = 299792458. # m / s
# --------------------------

d0 = 6.647 * 10**(-1) # dipole moment in minimum
r = 0.96966 * 10**(-10) # m, equilibrium distance 
mu = 16. * 1. / (16. + 1.) * da # in kg
rotational_constant = h / (8 * np.pi**2 * mu * c * r**2) / 100 # 100 to translate m**(-1) to cm**(-1)
print('rotational_constant: {0} cm-1'.format(rotational_constant))

energies, J = read_energies()

width = 1.5

temperatures = [30, 50, 70, 100]
for plot_number, temperature in enumerate(temperatures):
    transitions, intensities = model_spectra(temperature)

    ax = plt.subplot(2, 2, plot_number + 1)
    ax.set_title('T = ' + str(temperature) + 'K')
    ax.bar(transitions, intensities, width, color = 'blue', align = 'center')

plt.show()
#plt.savefig('rotational_spectra.png', bbox_inches = 'tight')


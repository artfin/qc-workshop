from __future__ import print_function

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from lib.general import read_energy_file, read_spectrum_file, show_spectra

# constants
cmtoj = 1.98630 * 10**(-23)
d0 = 6.647 * 10**(-1) # dipole moment in minimum
k = 1.38064852 * 10**(-23) # J / K

def save_spectra(filename, transitions_m, transitions_p):
    with open(filename, mode = 'w') as out:
        out.write('transitions corresponding to j = +1')
        for e in transitions_p:
            out.write(str(e) + '\n')
        out.write('='*30)
        out.write('transitions corresponding to j = -1')
        for e in transitions_m:
            out.write(str(e) + '\n')

def model_spectra(angular_momentum, base_energies, matrix_element, temperature):
    intensities = []
    for j, e1 in zip(angular_momentum, base_energies):
        intensities.append(d0**2 * matrix_element**2 * (j + 1) * np.exp(-e1 * cmtoj / (k * temperature)))
    return intensities

v0, J = read_energy_file('my_potential/energy.dat', vibrational_level = 0)
v1, J = read_energy_file('my_potential/energy.dat', vibrational_level = 1)

frequencies, matrix_elements = read_spectrum_file('vib-sp-my/spectrum.dat')

# transitions corresponding to j = +1
transitions_p = []
j_p = []
for en1, en2 in zip(v0, v1[1:]):
    transitions_p.append(en2 - en1)
for j1, j2 in zip(J, J[1:]):
    j_p.append(j1)

# transitions corresponding to j = -1
transitions_m = []
j_m = []
for en1, en2 in zip(v0[1:], v1):
    transitions_m.append(en2 - en1)
for j1, j2 in zip(J, J[1:]):
    j_m.append(j2)

width = 2.0

temperatures = [200, 250, 300, 350]
for plot_number, temperature in enumerate(temperatures):
    intensities_p = model_spectra(j_p, v0, matrix_elements[0], temperature)
    intensities_m = model_spectra(j_m, v0, matrix_elements[0], temperature)
    
    show_spectra(temperature, transitions_p, intensities_p)
    show_spectra(temperature, transitions_m, intensities_m)

    ax = plt.subplot(2, 2, plot_number + 1)
    ax.set_title('T = ' + str(temperature) + 'K')
    ax.bar(transitions_p, intensities_p, width, color = "blue")
    ax.bar(transitions_m, intensities_m, width, color = "red")
    
    ax.set_xlim([3100, 3900])

    red_patch = mpatches.Patch(color = 'red', label = 'dJ = -1')
    blue_patch = mpatches.Patch(color = 'blue', label = 'dJ = +1')

    plt.legend(handles = [red_patch, blue_patch])
    plt.grid()

plt.show()


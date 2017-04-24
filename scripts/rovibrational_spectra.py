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

v0, J = read_energy_file('my_potential/energy.dat', vibrational_level = 2)
v1, J = read_energy_file('my_potential/energy.dat', vibrational_level = 3)
v0_ex, J = read_energy_file('example_potential/energy.dat', vibrational_level = 2)
v1_ex, J = read_energy_file('example_potential/energy.dat', vibrational_level = 3)

frequencies, matrix_elements = read_spectrum_file('vib-sp-my/spectrum.dat')
frequencies_ex, matrix_elements_ex = read_spectrum_file('vib-sp-example/spectrum.dat')

# transitions corresponding to j = +1
transitions_p = []
transitions_p_ex = []
j_p = []
for en1, en2 in zip(v0, v1[1:]):
    transitions_p.append(en2 - en1)
for j1, j2 in zip(J, J[1:]):
    j_p.append(j1)
for en1, en2 in zip(v0_ex, v1_ex[1:]):
    transitions_p_ex.append(en2 - en1)

# transitions corresponding to j = -1
transitions_m = []
transitions_m_ex = []
j_m = []
for en1, en2 in zip(v0[1:], v1):
    transitions_m.append(en2 - en1)
for j1, j2 in zip(J, J[1:]):
    j_m.append(j2)
for en1, en2 in zip(v0_ex[1:], v1_ex):
    transitions_m_ex.append(en2 - en1)

width = 2.5

temperatures = [200, 250, 300, 350]
for plot_number, temperature in enumerate(temperatures):
    intensities_p = model_spectra(j_p, v0, matrix_elements[0], temperature)
    intensities_m = model_spectra(j_m, v0, matrix_elements[0], temperature)

    intensities_p_ex = model_spectra(j_p,v0_ex, matrix_elements_ex[0], temperature)
    intensities_m_ex = model_spectra(j_m, v0_ex, matrix_elements_ex[0], temperature)

    show_spectra(temperature, transitions_p, intensities_p)
    show_spectra(temperature, transitions_m, intensities_m)
    show_spectra(temperature, transitions_p_ex, intensities_p_ex)
    show_spectra(temperature, transitions_m_ex, intensities_m_ex)

    ax = plt.subplot(2, 2, plot_number + 1)
    ax.set_title('T = ' + str(temperature) + 'K')
    ax.bar(transitions_p, intensities_p, width, color = "blue")
    ax.bar(transitions_m, intensities_m, width, color = "blue")
    ax.bar(transitions_p_ex, intensities_p_ex, width, color = 'red')
    ax.bar(transitions_m_ex, intensities_m_ex, width, color = 'red')
    
    ax.set_xlim([3100, 3900])
    #ax.set_ylim([0, 2.25e-9])

    red_patch = mpatches.Patch(color = 'red', label = 'Empirical')
    blue_patch = mpatches.Patch(color = 'blue', label = 'Calculated')

    plt.legend(handles = [red_patch, blue_patch])
    plt.grid()

plt.show()


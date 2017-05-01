from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from lib.general import read_spectrum_file, show_spectra

# --------------------------
# CONSTANTS
h = 6.626070040*10**(-34) # J * s
k = 1.38064852 * 10**(-23) # J / K
da = 1.66053904 * 10**(-27) # da to kg
c = 299792458. # m / s
cmtoj = 1.98630 * 10**(-23)
# --------------------------

def read_energy(filename):
    with open(filename, mode = 'r') as inputfile:
        lines = inputfile.readlines()

    energies = []

    for line in lines:
        if len(line) < 2:
            continue

        data = line.split()

        if data[0].isdigit():
            energies.append(float(data[1]))

    return energies

def model_spectra(energies, matrix_elements, temperature):
    
    intensities = []
    for e, m in zip(energies, matrix_elements):
        intensities.append(m**2 * np.exp(-e * cmtoj / (k * temperature)) )
    return intensities

def norm_arr(s):
    return [_ / max(s) for _ in s]

def get_hitran_data():
    
    with open('../hitran_api/downloaded_data/oh_vib.dat', mode = 'r') as inputfile:
        lines = inputfile.readlines()

    freq_hitran = []
    lineint_hitran = []

    lower_level = [0, 1, 2] # lower level
    higher_level = [1, 2, 3] # higher level


    for line in lines:
        
        if len(line) < 3:
            continue

        data = line.split()

        for ll, hl in zip(lower_level, higher_level):

            #print('looking for transitions {0} -> {1}'.format(ll, hl))
                
            if 'v=' + str(ll) in data[3] and 'v=' + str(hl) in data[4]:
    
                lj = float(data[3].split('J=')[1].split(';')[0])
                hj = float(data[4].split('J=')[1].split(';')[0])

                if lj == hj:
                    freq_hitran.append(float(data[1]))
                    lineint_hitran.append(float(data[5]))

    return freq_hitran, lineint_hitran

energies = read_energy('../data/vib-sp-my/energy.dat')
energies_ex = read_energy('../data/vib-sp-example/energy.dat')

freq_hitran, lineint_hitran = get_hitran_data()
lineint_hitran = norm_arr(lineint_hitran)

for f, i in zip(freq_hitran, lineint_hitran):
    print('freq: {0}; intensity: {1}'.format(f, i))

frequencies, matrix_elements = read_spectrum_file('vib-sp-my/spectrum.dat')
frequencies_ex, matrix_elements_ex = read_spectrum_file('vib-sp-example/spectrum.dat')

intensities = model_spectra(energies, matrix_elements, temperature = 298.15)
intensities_ex = model_spectra(energies_ex, matrix_elements_ex, temperature = 298.15)
intensities = norm_arr(intensities)
intensities_ex = norm_arr(intensities_ex)

for f, i in zip(frequencies, intensities):
    print('freq: {0}; intensity: {1}'.format(f, i))

width = 2

ax = plt.subplot(2, 1, 1)
ax.grid()
ax.set_title('HITRAN. T = 298.15K')
ax.set_xlim(3000, 4000)
ax.bar(freq_hitran, lineint_hitran, width, color = 'k')

ax = plt.subplot(2, 1, 2)
ax.grid()
ax.set_title('Calculated. 298.15K')
ax.set_xlim(3000, 4000)
ax.bar(frequencies, intensities, width, color = 'blue')
ax.bar(frequencies_ex, intensities_ex, width, color = 'red')
    
red_patch = mpatches.Patch(color = 'red', label = 'Empirical')
blue_patch = mpatches.Patch(color = 'blue', label = 'Calculated')
ax.legend(handles = [red_patch, blue_patch])

plt.show()

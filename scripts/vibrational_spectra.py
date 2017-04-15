from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# --------------------------
# CONSTANTS
h = 6.626070040*10**(-34) # J * s
k = 1.38064852 * 10**(-23) # J / K
da = 1.66053904 * 10**(-27) # da to kg
c = 299792458. # m / s
# --------------------------

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def read_file(filename):
    with open('../data/' + filename, mode = 'r') as inputfile:
        lines = inputfile.readlines()
    
    frequency = []
    matrix_element = []

    for line in lines:
        if len(line) > 1:
            if is_float(line.split()[0]):
                frequency.append(float(line.split()[0]))
            if is_float(line.split()[2]):
                matrix_element.append(float(line.split()[2]))
   
    return frequency, matrix_element

def model_spectra(frequencies, matrix_elements, temperature):
    
    vibrational_summ = 0
    for frequency in frequencies:
        vibrational_summ += np.exp(- frequency * c * h / (k * temperature))
    
    intensities = []
    for n, frequency, matrix_element in zip(range(len(frequencies)), frequencies, matrix_elements):
        intensities.append(matrix_element**2 * np.exp(-frequency * h * c / (k * temperature)) / vibrational_summ)

    return intensities

frequencies, matrix_elements = read_file('vib-sp-my/spectrum.dat')
frequencies_ex, matrix_elements_ex = read_file('vib-sp-example/spectrum.dat')

width = 100
temperatures = [100, 300, 500, 700]
for plot_number, temperature in enumerate(temperatures):
    intensities = model_spectra(frequencies, matrix_elements, temperature)
    intensities_ex = model_spectra(frequencies_ex, matrix_elements_ex, temperature)
    print('intensities: {0}'.format(intensities))
    print('*'*30)
    ax = plt.subplot(2, 2, plot_number + 1)
    ax.set_xlim(0, 15000)
    ax.set_title('T = ' + str(temperature) + 'K')
    ax.bar(frequencies, intensities, width, color = 'blue')
    ax.bar(frequencies_ex, intensities_ex, width, color = 'red')

plt.show()

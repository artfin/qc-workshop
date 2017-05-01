from __future__ import print_function

from lib.general import is_float
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import numpy as np

# --------------------------
k = 1.38064852 * 10**(-23) # J / K
cmtoj = 1.98630 * 10**(-23)
# --------------------------

def get_hitran_data():
    with open('../hitran_api/downloaded_data/hcl.dat', mode = 'r') as inputfile:
        lines = inputfile.readlines()

    freqs_hitran = []
    ecoeffs_hitran = []
    lineint_hitran = []

    for line in lines:
        if len(line) > 1:
            data = line.split()
    
            if 'v=2' in data[3] and 'v=3' in data[4]:
                lower_j = data[3].split('J=')[-1]
                if int(lower_j) < 30:
                    freqs_hitran.append(float(data[1]))
                    ecoeffs_hitran.append(float(data[2]))
                    lineint_hitran.append(float(data[5]))

    freqs_hitran = freqs_hitran[1:]
    ecoeffs_hitran = ecoeffs_hitran[1:]
    lineint_hitran = lineint_hitran[1:]

    return freqs_hitran, ecoeffs_hitran, lineint_hitran

def populate_tex_table():
    with open('../tex/einstein_table/main.tex', mode = 'r') as inputfile:
        lines = inputfile.readlines()

    rows = []
    for index, line in enumerate(lines):
        if '\hline' in line:
            rows.append(index)

    append_line = rows[-2] + 1

    with open('../tex/einstein_table/main.tex', mode = 'w') as out:
        for index, line in enumerate(lines):
            if index < append_line:
                out.write(line)

        for j_from, j_to, freq1, freq2, e1, e2 in zip(lower_j, higher_j, frequencies, freqs_hitran, einstein_coefficients, ecoeffs_hitran):
            out.write('{0:.3f}'.format(freq1) + ' & ' + '{0:.3f}'.format(freq2) + ' & ' + str(j_from) + ' & ' + str(j_to) + ' & ' + '{0:.3f}'.format(e1) + ' & ' + '{0:.3f}'.format(e2) + ' \\\\ \n')
    
        out.write('\hline \n')

        for index, line in enumerate(lines):
            if index > append_line:
                out.write(line)

def read_spectrum():
    with open('../INFO/HCl/SP/spectrum.dat', mode = 'r') as inputfile:
        lines = inputfile.readlines()
    
    frequency = []
    mu_ij = []
    lower_j = []
    lower_e = []

    for line in lines:
        data = line.split()
        
        if not is_float(data[0]):
            continue
    
        frequency.append(float(data[0]))
        mu_ij.append(float(data[1]))
        lower_j.append(int(data[2]))
        lower_e.append(float(data[3]))

    return frequency, mu_ij, lower_j, lower_e

def norm_array(arr):
    m = max(arr)
    return [s / m for s in arr]

def model_einst(frequencies, mu_ij):
    einstein_coefficients = []

    for j_from, j_to, mu, transition_energy in zip(lower_j, higher_j, mu_ij, frequencies):
        if j_to > j_from: 
            S = (j_from + 1.0) / (2.0 * j_from + 3.0)
        else:
            S = (j_from) / (2.0 * j_from - 1.0)

        einstein_coefficients.append(3.137 * 10**(-7) * mu**2 * S * transition_energy**3)
        print("freq: {0}; J'': {1}; J': {2}; S: {3}; Einstein: {4}".format(transition_energy, j_from, j_to, S, einstein_coefficients[-1]))
        
    return einstein_coefficients

def norm_arr(s):
    return [_ / max(s) for _ in s]

def model_spectra(frequencies, lower_e, mu_ij, temperature, lineint_hitran):
   
    line_intensities = []
    for freq, le, lj, mu in zip(frequencies, lower_e, lower_j, mu_ij):
        N = (2 * lj + 1) * np.exp(- le * cmtoj / (k * temperature))
        intensity = N * mu

        line_intensities.append(intensity)
        
        print('frequency: {0}; line intensity: {1}'.format(freq, intensity))

    line_intensities = norm_arr(line_intensities)
    lineint_hitran = norm_arr(lineint_hitran)
    
    width = 1 
    ax = plt.subplot(2, 1, 1)
    ax.bar(freqs_hitran, lineint_hitran, width, color = 'k')
    ax.set_title('HITRAN. Temperature: 298.15K')
    ax.set_xlim(2400, 2900)
    ax.grid()
    
    ax = plt.subplot(2, 1, 2)
    ax.bar(frequencies, line_intensities, width, color = 'r')
    ax.set_title('Calculated. Temperature: 298.15K')
    ax.set_xlim(2400, 2900)
    ax.grid()

    plt.show()

frequencies, mu_ij, lower_j, lower_e = read_spectrum()
freqs_hitran, ecoeffs_hitran, lineint_hitran = get_hitran_data()

print('J": {0}'.format(lower_j))
higher_j = list(reversed(range(lower_j[0]))) + range(1, lower_j[0] + 1)
print("J': {0}".format(higher_j))

#einstein_coefficients = model_einst(frequencies, mu_ij)

spectra = model_spectra(frequencies, lower_e, mu_ij, 298.15, lineint_hitran)




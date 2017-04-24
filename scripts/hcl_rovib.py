from __future__ import print_function

from lib.general import is_float

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

def model_spectra(frequencies, mu_ij, lower_j, lower_e):
    intensities = []

    print('J": {0}'.format(lower_j))

    higher_j = list(reversed(range(lower_j[0]))) + range(1, lower_j[0] + 1)
    print("J': {0}".format(higher_j))

    for j, e in zip(lower_j, lower_e):
        intensity = (j + 1) / (2 * j + 1)

frequencies, mu_ij, lower_j, lower_e = read_spectrum()
model_spectra(frequencies, mu_ij, lower_j, lower_e)

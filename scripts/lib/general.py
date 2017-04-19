from __future__ import print_function

import os

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def read_spectrum_file(filename):
    #print('Given path to read from: {0}'.format('data/' + filename))

    with open('data/' + filename, mode = 'r') as inputfile:
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

def read_energy_file(filename, vibrational_level):
    #print('Given path to read from: {0}'.format('data/' + filename))
    
    with open('data/' + filename, mode = 'r') as inputfile:
        lines = inputfile.readlines()

    J = []
    energies = []

    for line in lines:
        if 'J' in line:
            J.append(float(line.split()[-1]))
        if line.split()[0].isdigit():
            if int(line.split()[0]) == vibrational_level:
                energies.append(float(line.split()[1]))
    
    return energies, J

def show_spectra(temperature, transitions, intensities):
    print('*'*30)
    print('Temperature: {0}'.format(temperature))
    for transition, intensity in zip(transitions, intensities):
        print('transition: {0}; intensity: {1}'.format(transition, intensity))
    print('*'*30 + '\n')


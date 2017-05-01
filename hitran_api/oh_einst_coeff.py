from __future__ import print_function

import matplotlib.pyplot as plt

with open('downloaded_data/oh_rot.dat') as inputfile:
    lines = inputfile.readlines()

freqs_hitran = []
ecoeffs_hitran = []
jlower_hitran = []
jhigher_hitran = []

for line in lines:
    if len(line) > 1:

        data = line.split()
        
        if 'v=0' not in data[3] and 'v=0' not in data[4]:
            continue

        lj = float(data[3].split('J=')[1].split(';')[0])
        hj = float(data[4].split('J=')[1].split(';')[0])

        if lj >= hj or lj > 20 or hj > 20:
            continue

        freqs_hitran.append(float(data[1]))
        ecoeffs_hitran.append(float(data[2]))
        
        jlower_hitran.append(lj)
        jhigher_hitran.append(hj)

for f, lj, hj, a in zip(freqs_hitran, jlower_hitran, jhigher_hitran, ecoeffs_hitran):
    print('freq: {0}; lower j: {1}; higher j: {2}; einst: {3}'.format(f, lj, hj, a))

print('*'*30)

with open('../data/my_potential/energy.dat') as inputfile:
    lines = inputfile.readlines()

levels_calc = []
j_values = []

for line in lines:
    if len(line) > 1:
        data = line.split()
        
        if data[0].isdigit():
            if int(data[0]) == 0:
                levels_calc.append(float(data[1]))
        
        if 'J =' in line:
            j_values.append(float(data[-1]))


freq_calc = []
jlower_calc = []
jhigher_calc = []
ecoeffs_calc = []

for l1, l2, j1, j2 in zip(levels_calc, levels_calc[1:], j_values, j_values[1:]):
    f = l2 - l1
    
    freq_calc.append(f)
    jlower_calc.append(j1)
    jhigher_calc.append(j2)

    s = (j1) / (2 * j1 + 1.)
    
    ecoeffs_calc.append(3.137 * 10**(-7) * f**3 * s)

for f, lj, hj, e in zip(freq_calc, jlower_calc, jhigher_calc, ecoeffs_calc):
    print('freq: {0}; lower j: {1}; higher j: {2}; einst: {3}'.format(f, lj, hj, e))













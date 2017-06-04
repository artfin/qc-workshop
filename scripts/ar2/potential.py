from __future__ import print_function
from pprint import pprint

import matplotlib.pyplot as plt

htocm =  219474.63 

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def read_potential(filename):
    with open(filename, mode = 'r') as inputfile:
        lines = inputfile.readlines()

    dist = []
    energy = []

    for line in lines:
        if len(line) > 1:
            data = line.split()
        
            if len(data) < 1:
                continue

            if is_number(data[0]):
                dist.append(float(data[0]))
                energy.append(float(data[1]))

    return dist, energy

dist_ci, potential_ci = read_potential('ar2_ci.dat')
dist_ccsd, potential_ccsd = read_potential('aug-cc-pvqz.dat')
dist_avtz, potential_avtz = read_potential('avtz.dat')

fig = plt.figure()
plt.rc('text', usetex = True)

lw = 1.5
plt.plot(dist_ci, potential_ci, color = '0.6', linestyle = 'solid', linewidth = lw)
plt.plot(dist_ccsd, potential_ccsd, color = '0.5', linestyle = 'dashed', linewidth = lw)
plt.grid(linestyle = ':', alpha = 0.7)
plt.show()

#with open('ar2_ci.dat', mode = 'w') as out:
    #for r, e in zip(dist, energy):
       #out.write(str(r) + ' ' + str(e) + '\n')

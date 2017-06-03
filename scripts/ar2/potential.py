from __future__ import print_function
from pprint import pprint

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

with open('../../molpro/tables/ar2_ci.tab', mode = 'r') as inputfile:
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

htocm =  219474.63 
energy = [(e - min(energy)) * htocm for e in energy]

for r, e in zip(dist, energy):
    print(r, e)

with open('ar2_ci.dat', mode = 'w') as out:
    for r, e in zip(dist, energy):
       out.write(str(r) + ' ' + str(e) + '\n')

from __future__ import print_function
from pprint import pprint

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

with open('energy.dat', mode = 'r') as inputfile:
    lines = inputfile.readlines()

v0 = []

for line in lines:
    if len(line) > 0:
        data = line.split()

        if is_number(data[0]):
            if float(data[0]) == 0:
                v0.append(float(data[1]))

pprint(v0[::2])
v0 = [s - v0[0] for s in v0]
pprint(v0[::2])
            

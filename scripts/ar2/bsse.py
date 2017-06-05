from __future__ import print_function
import numpy as np

htocm = 219474.63 # hartree to cm-1

with open('../../molpro/ar2/ar_bsse.tab', mode = 'r') as inputfile:
    lines = inputfile.readlines()

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

dist = np.array([])
e_uncorr = np.array([])
e_corr = np.array([])
bsse = np.array([])

for line in lines:
    if len(line) > 1:
        data = line.split()

        if len(data) > 1:
            if is_number(data[0]):
                dist = np.append(dist, float(data[0]))
                e_uncorr = np.append(e_uncorr, float(data[1]))
                e_corr = np.append(e_corr, float(data[2]))
                bsse = np.append(bsse, float(data[1]) - float(data[2]))

e_uncorr = [e - e_uncorr[-1] for e in e_uncorr]
e_corr = [e - e_corr[-1] for e in e_corr]

for d, u, c, b in zip(dist, e_uncorr, e_corr, bsse):
    print("distance: {0}; uncorrelated: {1}; correlated: {2}; bbse: {3}".format(d, u * htocm, c * htocm, b * htocm))

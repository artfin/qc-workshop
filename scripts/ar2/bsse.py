from __future__ import print_function
import numpy as np

htocm = 219474.63 # hartree to cm-1

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def read_file(filename, dim):
    with open(filename, mode = 'r') as inputfile:
        lines = inputfile.readlines()

    dist = np.array([])
    e_uncorr = np.array([])
    e_corr = np.array([])
    bsse = np.array([])

    for line in lines:
        if len(line) > 1:
            data = line.split()

            if len(data) > 1:
                if is_number(data[0]):
                    if dim == 0:
                        dist = np.append(dist, float(data[0]))
                        e_uncorr = np.append(e_uncorr, float(data[1]))
                        e_corr = np.append(e_corr, float(data[2]))
                        bsse = np.append(bsse, float(data[1]) - float(data[2]))
                    if dim == 1:
                        dist = np.append(dist, float(data[0]))
                        e_uncorr = np.append(dist, float(data[1]))
                        bsse = np.append(bsse, float(data[2]))

    print(bsse)

    for d, b in zip(dist, bsse):
        print("distance: {0}; bbse: {1}".format(d, b * htocm))


read_file('../../molpro/ar2/ar_bsse_pvdz.tab', dim = 0)
read_file('../../molpro/ar2/ar_bsse_pvtz.tab', dim = 1)

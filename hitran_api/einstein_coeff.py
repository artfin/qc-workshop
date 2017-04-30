from __future__ import print_function

import matplotlib.pyplot as plt

with open('downloaded_data/hcl.dat', mode = 'r') as inputfile:
    lines = inputfile.readlines()

freqs = []
einstein_coeffs = []
lower = []
higher = []

for line in lines:
    if len(line) > 1:
        data = line.split()
        freqs.append(float(data[1]))
        einstein_coeffs.append(float(data[2]))
        lower.append(data[3])
        higher.append(data[4])

for f, e, l, h in zip(freqs, einstein_coeffs, lower, higher):
    if 'v=2' in l and 'v=3' in h:
        print('f: {0}; e: {1}; l: {2}; h: {3}'.format(f, e, l, h))

#plt.bar(freqs, einstein_coeffs, width = 2)
#plt.grid()
#plt.show()


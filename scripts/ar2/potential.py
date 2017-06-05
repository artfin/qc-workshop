from __future__ import print_function
from pprint import pprint

import matplotlib.pyplot as plt
from scipy import interpolate 
from scipy.interpolate import interp1d
import numpy as np

htocm =  219474.63 

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def read_potential(filename, dim):
    with open(filename, mode = 'r') as inputfile:
        lines = inputfile.readlines()

    dist = []
    energy = []

    for line in lines:
        if len(line) > 1:
            data = line.split()
        
            if len(data) < 2:
                continue

            if is_number(data[0]):
                dist.append(float(data[0]))
                energy.append(float(data[1]))
    
    if dim == 1:
        print('Limit: {0}'.format(energy[-1]))
        energy = [(e - energy[-1]) * htocm for e in energy]
    else:
        print('Limit: {0}'.format(energy[-1]))
        energy = [e - energy[-1] for e in energy]

    return dist, energy

def read_energy(filename, level):
    
    with open(filename, mode = 'r') as inputfile:
        lines = inputfile.readlines()

    v0 = []
    for line in lines:
        if len(line) > 0:
            data = line.split()

            if is_number(data[0]):
                if int(data[0]) == level:
                    v0.append(float(data[1]))

    return v0

dist_ccsd, potential_ccsd = read_potential('../../molpro/tables/ar2_ccsd.tab', dim = 1)
dist_emp, potential_emp = read_potential('../../data/ar2/pec.dat', dim = 0)
dist_patkowski, potential_patkowski = read_potential('../../data/ar2/patkowski/aug-cc-pv5z.dat', dim = 0)
dist_slavcek, potential_slavcek = read_potential('../../data/ar2/slavcek/aug-cc-pv5z.dat', dim = 0)

v0 = read_energy('../../data/ar2/my_ar/energy.dat', level = 0)
v1 = read_energy('../../data/ar2/my_ar/energy.dat', level = 1)
v2 = read_energy('../../data/ar2/my_ar/energy.dat', level = 2)

fig = plt.figure()
plt.rc('text', usetex = True)
ax = plt.subplot(1, 1, 1)

x = np.linspace(3.3, 8, num = 100, endpoint = True)

ccsd = interp1d(dist_ccsd, potential_ccsd, kind = 'cubic')
emp = interp1d(dist_emp, potential_emp, kind = 'cubic')
pat = interp1d(dist_patkowski, potential_patkowski, kind = 'cubic')
slav = interp1d(dist_slavcek, potential_slavcek, kind = 'cubic')

lw = 1.5
l1, = ax.plot(x, ccsd(x), color = '0.55', linestyle = 'dashed', linewidth = lw)
l3, = ax.plot(x, pat(x), color = '0.4', linestyle = 'dotted', linewidth = lw)
l4, = ax.plot(x, slav(x), color = '0.7', linestyle = 'solid', linewidth = lw)

ax.scatter(dist_ccsd, potential_ccsd, marker = 'x', color = 'k')
ax.scatter(dist_slavcek, potential_slavcek, color = 'k', marker = '*')
ax.scatter(dist_patkowski, potential_patkowski, color = 'k', marker = 'P')

ax.set_xlim(3, 8)
ax.set_ylim(-100, 10)

#for index, e0, e1, e2 in zip(range(len(v0)), v0, v1, v2):
    #ax.axhline(y = e0 + min(potential_ccsd), color = 'k', xmin = 0.12, xmax = 0.22)
    #ax.axhline(y = e1 + min(potential_ccsd), color = 'k', xmin = 0.10, xmax = 0.29)
    #ax.axhline(y = e2 + min(potential_ccsd), color = 'k', xmin = 0.09, xmax = 0.36)

fig.legend((l1, l3, l4), (r'CCSD(T); \textit{aug-cc-pVQZ}', r'CCSD(T); \textit{aug-cc-pV5Z+spdfg}; K.Patkowski, G. Murdachaew, C. Fou and K. Szalewicz, Mol. Phys. \textbf{103}, 15, 2005', r'CCSD(T) \textit{aug-cc-pV5Z + spdfg}; including core electrons; P. Slavicek, R. Kalus, P. Paska, I. Odvarkova, O. Hobza and A. Malijevsky, J. Chem. Phys., \textbf{119}, 4, 2003'), 'lower center', ncol = 1, fancybox = True, shadow = True, prop = {'size': 'small'})

#fig.legend((l1, l2), (r'CCSD(T); \textit{aug-cc-pVQZ}', r'\textit{Empirical}; E.A. Colbourn and A. E. Douglas,  J. Chem. Phys., \textbf{65}, 5, 1976'), 'lower center', ncol = 3, fancybox = True, shadow = True, prop = {'size': 'large'})

ax.set_title(r'\textbf{Potential profiles}')
ax.grid(linestyle = ':', alpha = 0.7)
ax.set_xlabel(r'\textbf{r}, (angstrem)')
ax.set_ylabel(r'\textbf{U}, (cm$^{-1}$)')

plt.tight_layout(pad = 1.7, w_pad = 0.0, h_pad = -3.0)

plt.show()

#with open('ar2_ci.dat', mode = 'w') as out:
    #for r, e in zip(dist, energy):
       #out.write(str(r) + ' ' + str(e) + '\n')

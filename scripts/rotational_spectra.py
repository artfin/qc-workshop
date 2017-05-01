from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from lib.general import read_energy_file, show_spectra

# constants
cmtoj = 1.98630 * 10**(-23)

def read_hitran_data():
    with open('../hitran_api/downloaded_data/oh_rot.dat', mode = 'r') as inputfile:
        lines = inputfile.readlines()
    
    j_lower = []
    j_higher = []

    freq_hitran = []
    lineint_hitran = []

    for line in lines:
      
        data = line.split()

        if len(line) > 1:
            if 'v=0' in data[3] and 'v=0' in data[4]:
                #print(line) 
                jl = float(data[3].split('J=')[-1].split(';')[0])
                jh = float(data[4].split('J=')[-1].split(';')[0])
                        
                #if j_lower:
                    #if jl == j_lower[-1]:
                        #continue
                
                if jl == jh:
                    continue

                if jl > 20 or jh > 20:
                    continue
            
                if jl > jh:
                    continue

                j_lower.append(jl)
                j_higher.append(jh)
                    
                freq_hitran.append(float(data[1]))
                lineint_hitran.append(float(data[5]))
    
    return freq_hitran, j_lower, j_higher, lineint_hitran

def norm_arr(s):
    return [_ / max(s) for _ in s]

def model_spectra(angular_momentum, transition_energy, temperature):
    transitions = []
    intensities = []
    
    for j, e1, e2 in zip(angular_momentum, transition_energy, transition_energy[1:]):
        transitions.append(e2 - e1)
        intensities.append(d0**2 * (j + 1.0) / (2 * j + 3.0) * (2 * j + 1.0) * np.exp(-e1 * cmtoj / (k * temperature)))
        print('J transition: {0} -> {1}'.format(j, j+1))
        print('Transition: {0}'.format(e2 - e1))
        print('Going from energy level: {0}'.format(e1))
        print('Intensity: {0}'.format(intensities[-1]))
        print('*'*30)

    return transitions, norm_arr(intensities)

# --------------------------
# CONSTANTS
h = 6.626070040*10**(-34) # J * s
k = 1.38064852 * 10**(-23) # J / K
da = 1.66053904 * 10**(-27) # da to kg
c = 299792458. # m / s
# --------------------------

d0 = 6.647 * 10**(-1) # dipole moment in minimum
r = 0.96966 * 10**(-10) # m, equilibrium distance 
mu = 16. * 1. / (16. + 1.) * da # in kg
rotational_constant = h / (8 * np.pi**2 * mu * c * r**2) / 100 # 100 to translate m**(-1) to cm**(-1)
print('rotational_constant: {0} cm-1'.format(rotational_constant))

energies, J = read_energy_file('my_potential/energy.dat', vibrational_level = 0)
energies_ex, J_ex = read_energy_file('example_potential/energy.dat', vibrational_level = 0)

width = 0.7

transitions, intensities = model_spectra(J, energies, 298.15)
transitions_ex, intensities_ex = model_spectra(J_ex, energies_ex, 298.15)
freq_hitran, j_lower, j_higher, lineint_hitran = read_hitran_data()
lineint_hitran = norm_arr(lineint_hitran)
    
ax = plt.subplot(2, 1, 1)
ax.set_title('Calculated Spectrum. T = 298.15 K')
ax.bar(transitions, intensities, width, color = 'blue')
ax.bar(transitions_ex, intensities_ex, width, color = 'red')

ax.set_xlim([0, 400])

red_patch = mpatches.Patch(color = 'red', label = 'Empirical')
blue_patch = mpatches.Patch(color = 'blue', label = 'Calculated')
ax.legend(handles = [red_patch, blue_patch])
ax.grid()

ax = plt.subplot(2, 1, 2)
ax.set_title('HITRAN. T = 298.15 K')
ax.bar(freq_hitran, lineint_hitran, width, color = 'k')
ax.grid()
ax.set_xlim([0, 400])

plt.show()


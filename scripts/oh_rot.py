from __future__ import print_function

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

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
                print(line)
    return freq_hitran, j_lower, j_higher, lineint_hitran

def norm_arr(s):
    return [_ / max(s) for _ in s]

freq_hitran, j_lower, j_higher, lineint_hitran = read_hitran_data()
lineint_hitran = norm_arr(lineint_hitran)

for f, jl, jh, s in zip(freq_hitran, j_lower, j_higher, lineint_hitran):
    print('freq: {0}; j lower: {1}; j higher: {2}; S: {3}'.format(f, jl, jh, s))

plt.bar(freq_hitran, lineint_hitran, width = 1.5, color = 'k')
plt.grid()
plt.show()



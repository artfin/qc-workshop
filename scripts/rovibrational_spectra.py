import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def save_spectra(filename, transitions_m, transitions_p):
    with open(filename, mode = 'w') as out:
        out.write('transitions corresponding to j = +1')
        for e in transitions_p:
            out.write(str(e) + '\n')
        out.write('='*30)
        out.write('transitions corresponding to j = -1')
        for e in transitions_m:
            out.write(str(e) + '\n')

filename = '/home/artfin/Desktop/repos/qc-workshop/data/my_potential/energy.dat'
with open(filename, mode = 'r') as inputfile:
    lines = inputfile.readlines()

v0 = []
v1 = []

for line in lines:
    if line.split()[0].isdigit():
        if int(line.split()[0]) == 0:
            v0.append(float(line.split()[1]))
        if int(line.split()[0]) == 1:
            v1.append(float(line.split()[1]))

# transitions corresponding to j = +1
transitions_p = []
for en1, en2 in zip(v0, v1[1:]):
    transitions_p.append(en2 - en1)

# transitions corresponding to j = -1
transitions_m = []
for en1, en2 in zip(v0[1:], v1):
    transitions_m.append(en2 - en1)

height_p = [1] * len(transitions_p)
height_m = [1] * len(transitions_m)

width = 3

plt.bar(transitions_p, height_p, width, color = "blue")
plt.bar(transitions_m, height_m, width, color = "red")

red_patch = mpatches.Patch(color = 'red', label = 'dJ = -1')
blue_patch = mpatches.Patch(color = 'blue', label = 'dJ = +1')

plt.legend(handles = [red_patch, blue_patch])

plt.show()


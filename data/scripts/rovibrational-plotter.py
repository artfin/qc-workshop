import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

with open('rovibrational12.dat', mode = 'r') as inputfile:
    lines = inputfile.readlines()

transitions_p = []
transitions_m = []

switcher = 0
for line in lines:
    if switcher == 0:
        if is_number(line.split()[0]):
            transitions_p.append(float(line.split()[0]))
    
    if line[0] == '=':
        switcher = 1

    if switcher == 1:
        if is_number(line.split()[0]):
            transitions_m.append(float(line.split()[0]))

height_p = [1] * len(transitions_p)
height_m = [1] * len(transitions_m)

width = 3

plt.bar(transitions_p, height_p, width, color = "blue")
plt.bar(transitions_m, height_m, width, color = "red")

red_patch = mpatches.Patch(color = 'red', label = 'dJ = -1')
blue_patch = mpatches.Patch(color = 'blue', label = 'dJ = +1')

plt.legend(handles = [red_patch, blue_patch])

#plt.show()
plt.savefig("rovibrational12.png")


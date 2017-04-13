import matplotlib.pyplot as plt

with open('rotational_transitions.dat', mode = 'r') as inputfile:
    lines = inputfile.readlines()

transitions = []

for line in lines:
    transitions.append(float(line))

y = [1]*len(transitions)

width = 1

plt.bar(transitions, y, width, color = "blue")
#plt.show()

plt.savefig("rotational_transitions.png")


with open('energy.dat', mode = 'r') as inputfile:
    lines = inputfile.readlines()


v0 = []

for line in lines:
    if line.split()[0].isdigit():
        if int(line.split()[0]) == 0:
            v0.append(float(line.split()[1]))

transitions = []

for e1, e2 in zip(v0, v0[1:]):
    transitions.append(e2 - e1)

with open('rotational_transitions.dat', mode = 'w') as out:
    for transition in transitions:
        out.write(str(transition) + '\n')

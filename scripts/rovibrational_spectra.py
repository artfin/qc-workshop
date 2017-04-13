with open('energy.dat', mode = 'r') as inputfile:
    lines = inputfile.readlines()

v0 = []
v1 = []

for line in lines:
    if line.split()[0].isdigit():
        if int(line.split()[0]) == 1:
            v0.append(float(line.split()[1]))
        if int(line.split()[0]) == 2:
            v1.append(float(line.split()[1]))

# transitions corresponding to j = +1
transitions_p = []
for en1, en2 in zip(v0, v1[1:]):
    transitions_p.append(en2 - en1)

# transitions corresponding to j = -1
transitions_m = []
for en1, en2 in zip(v0[1:], v1):
    transitions_m.append(en2 - en1)

with open('rovibrational12.dat', mode = 'w') as out:
    out.write('transitions corresponding to j = +1')
    for e in transitions_p:
        out.write(str(e) + '\n')
    out.write('='*30)
    out.write('transitions corresponding to j = -1')
    for e in transitions_m:
        out.write(str(e) + '\n')

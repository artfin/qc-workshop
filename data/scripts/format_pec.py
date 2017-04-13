with open('pec_my.dat', mode = 'r') as inputfile:
	lines = inputfile.readlines()

distance = []
potential = []

for line in lines:
	if len(line.split()):
		distance.append(float(line.split()[0]))
		potential.append(float(line.split()[1]))

potential_min = abs(min(potential))

potential = [value + potential_min for value in potential]

with open('pec_norm.dat', mode = 'w') as out:
	for dist, value in zip(distance, potential):
		out.write(str(dist) +  ' ' + str(value) + '\n')


debye = 0.393456

with open('../../molpro/tables/molpro.table', mode = 'r') as inputfile:
    lines = inputfile.readlines()

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

dists = []
dips = []

for line in lines:
    if len(line.split()) > 1:
        if is_float(line.split()[0]):
            dists.append(float(line.split()[0]))
            dips.append(float(line.split()[4]))

with open('dip.dat', mode = 'w') as out:
    for dist, dip in zip(dists, dips):
        out.write(str(dist) + ' ' + str(dip / debye) + '\n')

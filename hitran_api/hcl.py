from hapi import *

import matplotlib.pyplot as plt

db_begin('data')

# to view parameters
#table = select('HCl', ParameterNames = ('nu', 'sw', 'a'), Conditions=('between', 'nu', 4000, 4100))

def norm_array(arr):
    m = max(arr)
    return [s / m for s in arr]

def trim_columns(nu, einsteint_coeffs, lower_nu, higher_nu):
    res_nu = []
    res_a = []
    for n, a in zip(nu, einsteint_coeffs):
        if n > lower_nu and n < higher_nu:
            res_nu.append(n)
            res_a.append(a)

    return res_nu, res_a

nu, einsteint_coeffs = getColumns('HCl', ['nu', 'a'])
nu, einsteint_coeffs = trim_columns(nu, einsteint_coeffs, 2300, 3000)

imp_nu = []
imp_ec = []

for f, e in zip(nu, einsteint_coeffs):
    if e > 30.0:
        print('freq: {0}; einstein: {1}'.format(f, e))
        imp_nu.append(f)
        imp_ec.append(e)

plt.bar(imp_nu, imp_ec, width = 2)
plt.show()



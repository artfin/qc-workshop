from hapi import *
import matplotlib.pyplot as plt

db_begin('data')

#fetch('CO2', 2, 1, 2000, 2100)
#nu, coef = absorptionCoefficient_Lorentz(SourceTables='CO2')

for plot_number, temperature in enumerate([150.0, 200.0, 250.0, 300.0]):
    nu, coef = absorptionCoefficient_Lorentz(SourceTables='OH', Environment={'p':1.0, 'T': temperature})
    ax = plt.subplot(2, 2, plot_number + 1)
    ax.set_title('T= ' + str(temperature) + 'K')
    ax.set_xlim(25, 600) 
    plt.plot(nu, coef)

plt.show()
#plt.savefig('spectra/oh.png')

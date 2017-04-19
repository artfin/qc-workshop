from hapi import *
from pylab import show, plot, subplot, xlim, ylim, title, legend, xlabel, ylabel, hold, grid

db_begin('data')

x, y = getStickXY('OH')
plot(x, y)
xlim([50, 400])

# for rovibrational band of OH
#ylim([0, 10e-20])

grid()
show()

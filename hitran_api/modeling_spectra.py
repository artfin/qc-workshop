from hapi import *
from pylab import show, plot, subplot, xlim, ylim, title, legend, xlabel, ylabel, hold, grid

db_begin('data')

x, y = getStickXY('OH')
plot(x, y)
xlim([3200, 3850])
ylim([0, 10e-20])
grid()
show()

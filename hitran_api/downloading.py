from hapi import *

# choosing a folder for our local database
db_begin('data')

# to get additional info on function 'fetch'
# getHelp(fetch)

fetch('OH', 13, 1, 0, 12000)
# TableName 
# M -- HITRAN  molecule number
# I -- HITRAN isotopologue number
# numin -- lower wavenumber bound
# numax -- upper wavenumber bound


# specifying a subset of columns to display
#Cond = ('AND', ('BETWEEN', 'nu', 0, 6000), ('>=', 'sw', 1e-20))
#select('OH', Conditions = Cond) 





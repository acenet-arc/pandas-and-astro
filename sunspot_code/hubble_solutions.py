# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 15:18:46 2019

@author: rdickson
"""

def distance_from_modulus(dist_mod):
    # Reference: https://lco.global/spacebook/what-is-distance-modulus/
    parsecs = 10**((dist_mod+5)/5)
    return parsecs

# Ingest the data
import pandas
data_columns = ['galaxy', 'supernova', 'm', 'sig_m',  
                'dist_mod', 'sig_dist_mod', 'M', 'sig_M', 'velocity']
data = pandas.read_csv('hubble_data.dat', delim_whitespace=True, index_col=1,
                       names=data_columns)

# Add column for distance
distance = distance_from_modulus(data['dist_mod'])
data['distance'] = distance/1.e6   # distance in megaparsecs, Mpc
#print(data)

# Plot distance (Mpc) versus velocity (unknown units, maybe km/sec)
import matplotlib.pyplot as plt
plt.plot(data['distance'],data['velocity'], 'o')
plt.xlabel('distance / Mpc')
plt.xlim(0.0, 40.0)
plt.ylabel('velocity')
plt.ylim(0.0, 3000.)
plt.show()

# Linear fit: velocity ~= H*distance (+intercept)
import numpy
nplm = numpy.polyfit(data.distance, data.velocity, 1)
# numpy.polyfit output is [coef_n, ..., coef_1, coef_0]
print("Slope:", nplm[0], "Intercept:", nplm[1]) 
velocity_fit = nplm[0]*data.distance + nplm[1]

plt.plot(data.distance, velocity_fit, 'r-')
plt.show


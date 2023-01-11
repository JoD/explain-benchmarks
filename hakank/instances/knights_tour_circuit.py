"""
Knights tour in cpmpy.

Create a knights path in a n x n matrix for all integers from 1..n*n-1.
The integer n*n is placed whatever it may fit...

This model use the circuit constraints and then we use extract_tour
for getting the proper tour.

Note that the numbers are 0..n*n-1 (since circuit requires that)

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys,math
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *


#
# Extract the tour from the circuit x
#
def extract_tour(x):
    n = len(x)
    k = 0
    tour = np.array([[-1 for i in range(n)] for j in range(n)])
    tour[0][0] = k
    next = x[0,0]
    while k < n*n:
        i = math.floor(next/ n)
        j = (next) % n
        tour[i][j] = k
        next = x[i,j]
        k += 1
    

def knights_tour_circuit(n=4,num_sols=0):

    # Since we use circuit we have to use 0..n*n-1 instead
    x = intvar(0,n*n-1,shape=(n,n),name="x")    
    x_flat = x.flat

    model = Model(
                 AllDifferent(x),
                 Circuit(x_flat),
                 )

    d = [-2,-1,1,2]
    for i in range(n):
        for j in range(n):
            dom = [ (i+a)*n + j+b for a in d for b in d if
                    abs(a) + abs(b) == 3 and
                    i+a >= 0 and i+a < n and
                    j+b >= 0 and j+b < n
                    ]
            model += [member_of(dom,x[i,j])]

    return model


# Note: this only works for even n
def get_model(seed=0):
    import random
    random.seed(seed)
    n = random.choice(list(ni for ni in range(6,10+1) if ni % 2 == 0))
    return    knights_tour_circuit(n,1)


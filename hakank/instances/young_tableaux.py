"""
Young tableaux in cpmpy.

See 
http://mathworld.wolfram.com/YoungTableau.html
and
http://en.wikipedia.org/wiki/Young_tableau
'''
The partitions of 4 are
 {4}, {3,1}, {2,2}, {2,1,1}, {1,1,1,1}

And the corresponding standard Young tableaux are:

1.   1 2 3 4

2.   1 2 3         1 2 4    1 3 4
     4             3        2

3.   1 2           1 3
     3 4           2 4

4    1 2           1 3      1 4 
     3             2        2 
     4             4        3

5.   1
     2
     3
     4
'''

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys, math
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *


def get_model():
    return young_tableaux()
    
    
def young_tableaux(n = 5):

    # Decision variables
    x = intvar(1,n+1,shape=(n, n), name="x")
    x_flat = x.flat
    
    p = intvar(0, n+1,shape=n, name="p")

    model = Model()

    # 1..n is used exactly once
    for i in range(1, n + 1):
        model += [count(x_flat, i, 1)]

    model += [x[0, 0] == 1]

    # row wise
    for i in range(n):
        model += [x[(i, j)] >= x[(i, j - 1)] for j in range(1,n)]
        # for j in range(1, n):
        #     model += [x[(i, j)] >= x[(i, j - 1)]]

    # column wise
    for j in range(n):
        model += [x[(i, j)] >= x[(i - 1, j)] for i in range(1,n)]
        # for i in range(1, n):
        #    model += [x[(i, j)] >= x[(i - 1, j)]]

    # calculate the structure (the partition)
    for i in range(n):
        model += [p[i] == sum([ x[i,j] <= n for j in range(n)  ])]

    model += [sum(p) == n]

    for i in range(1, n):
        model += [p[i - 1] >= p[i]]

    return model

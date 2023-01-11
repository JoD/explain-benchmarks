"""
DONALD + GERALD = ROBERT problem in cpmpy.

Classic alphametic problem.

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my CPMpy page: http://www.hakank.org/cpmpy/
"""
from cpmpy import *
import numpy as np
from instances.cpmpy_hakank import *

def donald_gerald_robert_v1():
    n = 10
    x = intvar(0,9,shape=10,name="x")
    d,o,n,a,l,g,e,r,b,t = x

    model = Model([AllDifferent(x),

                   100000*d + 10000*o + 1000*n + 100*a + 10*l + d 
                   + 100000*g + 10000*e + 1000*r + 100*a + 10*l + d
                   == 100000*r + 10000*o + 1000*b + 100*e + 10*r + t,
                   d > 0,
                   g > 0,
                   r > 0,
                   ])
    
    return model


def get_model(seed=0):
    return donald_gerald_robert_v1()


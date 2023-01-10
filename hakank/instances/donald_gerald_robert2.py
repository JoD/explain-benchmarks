"""
DONALD + GERALD = ROBERT problem in cpmpy.

Classic alphametic problem.

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my CPMpy page: http://www.hakank.org/cpmpy/
"""
from cpmpy import *
import numpy as np
from instances.cpmpy_hakank import *



def donald_gerald_robert_v2():
    n = 10
    x = intvar(0,9,shape=10,name="x")
    d,o,n,a,l,g,e,r,b,t = x

    carries = intvar(0,1,shape=6,name="carries")
    c1,c2,c3,c4,c5,c6 = carries

    model = Model([AllDifferent(x),
                   d + d == 10 * c1 + t,
                   c1 + l + l == 10 * c2 + r,
                   c2 + a + a == 10 * c3 + e,
                   c3 + n + r == 10 * c4 + b,
                   c4 + o + e == 10 * c5 + o,
                   c5 + d + g == 10 * c6 + r,

                   d > 0,
                   g > 0,
                   r > 0,
                   c6 == 0, # must be 0 since R is the first digit
                   ])
    
    return model


def get_model():
    return donald_gerald_robert_v2()

"""
Remainder problem in cpmpy.

'''
11.  Is there a number which when divided by 3 gives a remainder of 1;
when divided by 4, gives a remainder of 2; when divided by 5, gives a
remainder of 3; and when divided by 6, gives a remainder of 4?
(Kordemsky)
'''


Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my CPMpy page: http://www.hakank.org/cpmpy/

"""
from cpmpy import *
import numpy as np
from instances.cpmpy_hakank import *


def remainder_problem():
    Max = 10000
    v = intvar(1,Max,shape=5,name="v")
    X,A,B,C,D = v

    model = Model([
        X == A*3 + 1,
        X == B*4 + 2,
        X == C*5 + 3,
        X == D*6 + 4,
        ])

    return model

def get_model():
    return remainder_problem()

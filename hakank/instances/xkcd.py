"""
xkcd problem in cpmpy.

See http://xkcd.com/287/

Some amount (or none) of each dish should be ordered to give a total 
of exact 15.05

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my CPMpy page: http://www.hakank.org/cpmpy/

"""
from cpmpy import *
import numpy as np
from instances.cpmpy_hakank import *

def get_model(seed=0):
    return xkcd()

def xkcd(price=[215, 275, 335, 355, 420, 580],z=1505):
    x = intvar(0,100,shape=len(price),name="x")
    model = Model(
        z == sum(x* price)
        )

    return model

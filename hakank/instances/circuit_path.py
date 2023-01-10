"""
Decomposition of the circuit_path constraint in cpmpy

circuit_path(x,path) is a variant of (my_)circuit were the
path is visible.

The 'orbit' method that is used here is based on some
observations on permutation orbits.

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
from cpmpy import *
from cpmpy.solvers import *
import numpy as np
from cpmpy_hakank import *

def circuit_path_test(n=5):

    x = intvar(0, n-1,n,name='x')
    z = intvar(0, n-1,shape=n,name='z')    
    model = Model (
        my_circuit_path(x,z),
        )

    return model

def get_model(seed=0):
    import random
    random.seed(seed)
    circuit_size = int(round(random.uniform(5, 30)))
    return circuit_path_test(circuit_size)


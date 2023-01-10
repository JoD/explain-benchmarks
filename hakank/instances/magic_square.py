"""
Magic squares in cpmpy

See https://en.wikipedia.org/wiki/Magic_square


Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys,math
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from cpmpy_hakank import *


def magic_square(n=4,num_sols=0,symmetry_breaking=False,num_procs=1):
    print(f"\n\nn:{n} num_sols:{num_sols}")

    m = n*n
    x = intvar(1,m,shape=(n, n), name='x')
    x_flat = x.flat
    
    total = math.ceil(n*(m+1)/2)
    print("total:",total)
    
    model = Model (
        [
        AllDifferent(x),
        [ sum(row) == total for row in x],
        [ sum(col) == total for col in x.transpose()],               
        # sum([ x[i,i] for i in range(n)]) == total, # diag 1
        sum(x.diagonal()) == total,
        sum([ x[i,n-i-1] for i in range(n)]) == total, # diag 2
        ]
        )

    if symmetry_breaking:
        model += [frenicle(x,n)]

    return model


def get_model(seed=0):
    import random
    random.seed(seed)
    n = int(round(random.uniform(3, 15)))
    # Just first solution (it's faster without symmetry breaking).
    return magic_square(n,symmetry_breaking=False)



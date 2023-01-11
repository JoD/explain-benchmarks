"""
Global constraint nvalue in cpmpy.

Clobal Constraint Catalog
http://www.emn.fr/x-info/sdemasse/gccat/Cnvalue.html
'''
Purpose 
   NVAL is the number of distinct values taken by the variables of the collection VARIABLES
Example
  (4,<3,1,7,1,6>)

The nvalue constraint holds since its first argument NVAL=4 is set to the number of distinct
values occurring within the collection <3,1,7,1,6>.
'''

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *


def nvalue_test(n=5):
    x = intvar(1,n,shape=n,name="x")
    m = intvar(0,n,name="m" ) # number of distinct values

    # constraints
    model = Model(nvalue(m,x))
    return model

def get_model(seed=0):
  n = 5
  return nvalue_test(n)

"""
Global constraint among in cpmpy.
'''
Requires exactly m variables in x to take one of the values in v.
'''


Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *

def among_test():

  n = 5 # length of x
  m = 3 # number of values
  v = [1,5,8]

  # variables
  x = intvar(1,8,shape=n,name="x")

  # constraints  
  model = Model(among(m, x,v))

  return model

def get_model(seed=0):
  return among_test()

"""
Global constraint global_contiguity in Z3

From Global Constraint Catalogue
http://www.emn.fr/x-info/sdemasse/gccat/Cglobal_contiguity.html
'''
Enforce all variables of the VARIABLES collection to be assigned to 0 or 1. 
In addition, all variables assigned to value 1 appear contiguously.

Example:
(<0,1,1,0>)

The global_contiguity constraint holds since the sequence 0 1 1 0 contains 
no more than one group of contiguous 1.
'''

Here we also shows the start and end positions of the 1's.
Note that this implementation assumes that there is at least one 1.

See contiguity_regular.py for another implementation (using regular constraint)
without this assumption.


Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from cpmpy_hakank import *


#
# Global_contiguity:
# Enforce that all 1s must be in a contiguous group.
# Assumption: There must be at least one 1.
#
def global_contiguity(x,start,end):
  n = len(x)
  constraints = [start<=end]
  for i in range(n):
    constraints += [((i >= start) & (i <= end)) == x[i]]
  return constraints


def global_contiguity_test(n=4):
  print("n:",n)
  
  x = boolvar(shape=n,name="x")
  start = intvar(0,n-1,name="start")
  end = intvar(0,n-1,name="end")  

  model = Model(global_contiguity(x,start,end))

  return model

def get_model():           
  n = 4
  return global_contiguity_test(n)

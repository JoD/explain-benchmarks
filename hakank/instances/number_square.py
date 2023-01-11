"""
Number square problem in cpmpy.

From Pascal Van Henrentyck 'The OPL Optimization Programming Language', 
page 32:
'''
Consider finding an eight digit number that is a square and remains a square
when 1 is concatenated in front of its decimal notation.
'''

There are two solutions:

  n = 23765625
  x = 4875
  y = 11125

  n = 56250000
  x = 7500
  y = 12500



Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys,math
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *


def number_square():

    
    n = intvar(10000000,99999999,name="n")
    x = intvar(0,20000,name="x")
    y = intvar(0,20000,name="y")

    model = Model([n == x*x, 100000000+n ==y*y]
                  )

    return model

def get_model(seed=0):
  return number_square()

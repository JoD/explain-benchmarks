"""
Generate balanced brackets in cpmpy.

This model generates balanced brackets of size m*2.

The number of generated solutions for m:

 m        #
 ----------
  1       1
  2       2
  3       5
  4      14
  5      42
  6     132
  7     429
  8    1430
  9    4862
 10   16796
 11   58786
 12  208012
 13  742900

Which is - of course - the Catalan numbers:
http://oeis.org/search?q=1#2C2#2C5#2C14#2C42#2C132#2C429#2C1430#2C4862#2C16796#2C58786#2C208012&language=english&go=Search
http://oeis.org/A000108


This cpmpy model was written by Hakan Kjellerstrand (hakank@gmail.com)
See also my cpmpy page: http://hakank.org/cpmpy/
  
"""
from cpmpy import *
import numpy as np
from instances.cpmpy_hakank import *
from cpmpy.solvers import *
from ortools.sat.python import cp_model as ort

def brackets(m,do_print=False,num_sols=0):
  
    model = Model() 
    n = m*2

    s = ["[","]"]

    # For cumulative (c):
    # +1 if x[i] = "["
    # -1 if x[i] = "]"
    # t = cpm_array([-1,1]) # This don't work
    t = intvar(-1,1,shape=2,name="t")    
    model += (t[0] == 1,t[1] == -1)

    # 0: "[", 1: "]"
    x = boolvar(shape=n,name="x")
    c = intvar(0,n,shape=n,name="c") # counter (cumulative)
    
    # constraints
    
    # start sequence
    model += [x[0] == 0,
              c[0] == 1]

    # cumulative
    for i in range(1,n):
        model += (c[i] == c[i-1] + t[x[i]])

    model += (x[n-1] == 1)
    model += (c[n-1] == 0) # end sequence

    # Redundant constraint: This might make it faster (but it don't)
    model += (x.sum() == m)

    return model

def get_model(seed=0):
  import random
  random.seed(seed)
  bracket = random.choice(list(i for i in range(1,11+1)))
  return brackets(bracket)
  
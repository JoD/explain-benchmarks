"""
Magic sequence in cpmpy.
 
http://www.dcs.st-and.ac.uk/~ianm/CSPLib/prob/prob019/spec.html
'''
A magic sequence of length n is a sequence of integers x0 . . xn-1 between 
0 and n-1, such that for all i in 0 to n-1, the number i occurs exactly xi 
times in the sequence. For instance, 6,2,1,0,0,0,1,0,0,0 is a magic sequence 
since 0 occurs 6 times in it, 1 occurs twice, ...
'''

Cf autoref.py for a similar (but not identical) problem.

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *

def magic_sequence(n=10):
  #print("n:",n)
  model = Model()

  x = intvar(0,n-1,shape=n,name="x")

  # constraints
  for i in range(n):
    model += [x[i] == sum([x[j] == i for j in range(n)])]

  model += [sum(x) == n]
  model += [sum([x[i]*i for i in range(n)]) == n]

  return model

def get_model(seed=0):
  import random
  random.seed(seed)
  n = int(round(random.uniform(10, 50)))
  return magic_sequence(n)



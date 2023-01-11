"""
Talisman Square in cpmpy
http://mathworld.wolfram.com/TalismanSquare.html
'''
An n×n array  of the integers from 1 to n^2 such that the difference between 
any one integer and its neighbor (horizontally, vertically, or diagonally, without 
wrapping around) is greater than or equal to some value k is called a (n,k)-talisman 
square. 
'''

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *


def talisman_square(n=5,k=2):
  model = Model()
  
  x = intvar(1,n*n,shape=(n,n),name="x")
   
  model += (AllDifferent([x[(i,j)] for i in range(n) for j in range(n)]))

  for i in range(1,n):
    for j in range(1,n):
      model += (abs(x[i,j]-x[i-1,j]) >= k)
      model += (abs(x[i,j]-x[i,j-1]) >= k)

  for i in range(n-1):
    for j in range(n-1):
      model += (abs(x[i,j]-x[i+1,j]) >= k)
      model += (abs(x[i,j]-x[i,j+1]) >= k)

  # symmetry breaking
  model += (x[0,0] == 1)

  return model

def get_model(seed=0):
  n = 4
  k = 6
  return talisman_square(n,k)


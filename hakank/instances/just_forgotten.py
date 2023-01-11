"""
Just forgotten puzzle (Enigma 1517) in cpmpy.

From http://www.f1compiler.com/samples/Enigma 201517.f1.html
'''
Enigma 1517 Bob Walker, New Scientist magazine, October 25, 2008.

Joe was furious when he forgot one of his bank account numbers.
He remembered that it had all the digits 0 to 9 in some order,
so he tried the following four sets without success:

  9 4 6 2 1 5 7 8 3 0
  8 6 0 4 3 9 1 2 5 7
  1 6 4 0 2 9 7 8 5 3
  6 8 2 4 3 1 9 0 7 5

When Joe finally remembered his account number, he realised that
in each set just four of the digits were in their correct position
and that, if one knew that, it was possible to work out his
account number. What was it?
'''
 
This cpmpy model was written by Hakan Kjellerstrand (hakank@gmail.com)
See also my cpmpy page: http://hakank.org/cpmpy/
  
"""
from cpmpy import *
import cpmpy.solvers
import numpy as np
from instances.cpmpy_hakank import *


def just_forgotten():

  model = Model()
  
  # data
  rows = 4
  cols = 10
  # The four tries
  a = [[9, 4, 6, 2, 1, 5, 7, 8, 3, 0],
       [8, 6, 0, 4, 3, 9, 1, 2, 5, 7],
       [1, 6, 4, 0, 2, 9, 7, 8, 5, 3],
       [6, 8, 2, 4, 3, 1, 9, 0, 7, 5]]

  # variables
  x = intvar(0,9,shape=cols,name="x")

  #
  # constraints
  #
  model += [AllDifferent(x)]

  for r in range(rows):
    model += [sum([x[c] == a[r][c] for c in range(cols)]) == 4]

  return model

def get_model(seed=0):
  return just_forgotten()

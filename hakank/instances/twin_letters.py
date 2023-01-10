"""
Twin letters problem in cpmpy.

From http://www.comp.nus.edu.sg/~henz/projects/puzzles/digits/index.html
'''
Twin Letters    

In the following puzzle, there are ten pairs of
letters to be assigned to the same digit so that the multiplication
(including intermediate results) is correct. Can you find out the
pairs and their values?

        A B C
 *      D E F
 ____________
        G H I
      J K L
    M N O
 ____________
    P Q R S T
'''

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from cpmpy_hakank import *

def twin_letters():


  n = 20

  # variables
  x = intvar(0,9,shape=n,name="x")
  A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T = x

  C1 = boolvar(name="C1")
  C2 = intvar(0,2,name="C2")
  C3 = boolvar(name="C3")

  # constraints

  model = Model()

  # exact 2 occurrences of each digit
  # for i in range(9+1):
  #   model += (count2(sol, i, x) == 2)
  model += (global_cardinality_count(x,[2 for i in range(10)]))

  model += (
             100*G + 10*H + I +
    1000*J + 100*K + 10*L +
    10000*M + 1000*N + 100*O ==
    10000*P + 1000*Q + 100*R + 10*S + T
     )
    
  model += ((100*D + 10*E + F)*C == 100*G + 10*H + I)
  model += ((100*D + 10*E + F)*B == 100*J + 10*K + L)
  model += ((100*D + 10*E + F)*A == 100*M + 10*N + O)
    
  model += ((100*A + 10*B + C) * (100*D + 10*E + F) ==
            10000*P + 1000*Q + 100*R + 10*S + T)

  #  carry restrictions
  model += (T == I)
  model += (S + 10*C1 == H + L)
  model += (R + 10*C2 == G + K + O + C1)
  model += (Q + 10*C3 == J + N + C2)
  model += (P         == M + C3)

  return model

def get_model():
  return twin_letters()

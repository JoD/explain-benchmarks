"""
Cabling problem in cpmpy

From https://yurichev.com/blog/cabling_Z3/
'''
Take a rack cabinet, like this one:
  [ an image ]
  
Let's say, there are 8 1U devices, maybe servers, routers and whatnot, named
as A, B, C, D, E, F, G, H. Devices must be connected by cables: probably
twisted pair or whatever network engineers using today. Some devices must be
connected by several cables (2 cables, 3 or 4):

A <--- 1 cable  ---> H
A <--- 2 cables ---> E
B <--- 4 cables ---> F
C <--- 1 cable  ---> G
C <--- 1 cable  ---> D
C <--- 1 cable  ---> E
D <--- 3 cables ---> H
G <--- 1 cable  ---> H

The problem: how we can place these 8 devices in such an order, so that sum
of all cable lengths would be as short as possible?
'''

Here are two models:
- cabling1: A port of the original Z3 model
- cabling2: A more general approach.
            This model also shows all the 48 optimal
            solutions (length = 19)

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *

def diff(x, y):
    return abs(x-y)

#
# A more general model
#
def cabling_2(min_val=None):
  #print("min_val:", min_val)
  model = Model()

  n = 8
  # A <--- 1 cable  ---> H
  # A <--- 2 cables ---> E
  # B <--- 4 cables ---> F
  # C <--- 1 cable  ---> G
  # C <--- 1 cable  ---> D
  # C <--- 1 cable  ---> E
  # D <--- 3 cables ---> H
  # G <--- 1 cable  ---> H
  A,B,C,D,E,F,G,H = list(range(n))
  cable_struct = [[A,H,1], 
                  [A,E,2],
                  [B,F,4],
                  [C,G,1],
                  [C,D,1],
                  [C,E,1],
                  [D,H,3],
                  [G,H,1]
                  ]

  x = intvar(0,n-1,shape=n,name="x")
  t = intvar(1,n*n,shape=len(cable_struct),name="t")
  final_sum = intvar(0,n*n,name="final_sum")


  # all "devices" has distinct positions in rack:
  model += [AllDifferent(x),
            final_sum == sum(t)]

  for i in range(n):
    a,b,num = cable_struct[i]
    model += [t[i] == abs(x[a]-x[b])*num]

  if min_val == None:
    model.minimize(final_sum)
  else:
    model += [final_sum == min_val]

  return model

def get_model():
  return cabling_2()


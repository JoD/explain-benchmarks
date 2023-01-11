"""
Coin application in cpmpy.

From 'Constraint Logic Programming using ECLiPSe'
pages 99f and 234 ff.
The solution in ECLiPSe is at page 236.
'''
What is the minimum number of coins that allows one to pay _exactly_
any amount smaller than one Euro? Recall that there are six different
euro cents, of denomination 1, 2, 5, 10, 20, 50
'''

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *


def coins3(denominations=[1, 2, 5, 10, 25, 50],num_coins_val=0):
  #print("num_coins_val:",num_coins_val)
  
  # data
  # n = 6  # number of different coins
  # variables = [1, 2, 5, 10, 25, 50]
  n = len(denominations)

  # declare variables
  x = intvar(0,99,shape=n,name="x")
  num_coins = intvar(0, 99, name="num_coins")

  if num_coins_val == 0:
      model = Model(minimize=num_coins)
  else:
      model = Model([num_coins==num_coins_val])


  # constraints

  # number of used coins, to be minimized
  model += [num_coins == sum(x)]

  # Check that all changes from 1 to 99 can be made.
  for j in range(1, 100):
    tmp = intvar(0,99,shape=n)
    model += [sum(tmp*denominations) == j]
    model += [tmp[i] <= x[i] for i in range(n)]

  return model

def get_model(seed=0):
  
  denominations=[1, 2, 5, 10, 25, 50]
  # denominations=[1, 5, 10, 25, 50]
  #print("denominations:", denominations),
  return coins3(denominations,0)

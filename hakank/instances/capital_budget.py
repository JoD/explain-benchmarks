"""
Capital budgeting in cpmpy

Winston 'Operations Research', page 478: Capital budgeting 

And some extra constraint (page 479):
 either one of: 
 - can only make two investments
 - if investment 2 then investment 1
 - if investment 2 then not investment 4


Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my CPMpy page: http://www.hakank.org/cpmpy/

"""
import os,random
from cpmpy import *
import numpy as np
from instances.cpmpy_hakank import *


def capital_budget(cons=None):

  budget = 14
  npv = [16,22,12,8]
  cash_flow = [5,7,4,3]
  n = 4

  # variables

  x = boolvar(shape=n,name="x") # x[i] = 1 if investments i
  z = intvar(0,1000,name="z")

  # constraints
  model = Model([
    # the sum of all choosen investments must be less than the budget
    sum(x*cash_flow) <= budget,   
    z == sum(x*npv)
    ])

  #
  # the extra constraints
  #

  # only two investments
  if cons == 0:
    #print("extra constraint: only two investments")
    model += (sum(x) == 2)

  # if investment 2 -> investment 1
  if cons == 1:
    #print("extra constraint: if investment 2 -> investment 1")
    model += (x[1]).implies(x[0] == 1),
    # model += x[0] >= x[1],  # alternative (Integer Programming) way 

  # if investment 2 then not investment 4
  if cons == 2:
    #print("extra constraint: if investment 2 -> not investment 4")
    model += (x[1] == 1).implies(x[3] == 0),
    # model += (x[3] + x[1] <= 1),  # IP way

  model.maximize(z)

  return model

def get_model(seed=0):
  return capital_budget(2)

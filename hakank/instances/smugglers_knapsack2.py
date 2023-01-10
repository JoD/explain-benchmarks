"""
Smuggler's knapsack problem in cpmpy.

Marriott & Stucker: 'Programming with constraints', page  101f, 115f

Smuggler's knapsack.
  
A smuggler has a knapsack with a capacity of 9 units.
            Unit       Profit
Whisky:     4 units    15 dollars
Perfume:    3 units    10 dollars
Cigarettes: 2 units     7 dollars

What is the optimal choice?


Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys, math,string
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from cpmpy_hakank import *

#
# General approach.
# 
def smugglers_knapsack2(units,values,max_val):

    n = len(units)

    # variables
    x = intvar(0,100,shape=n,name="x")
    profit = intvar(0,1000,name="profit")

    model = Model([sum(x*units) <= max_val,
                   profit == sum(x*values),
                   ],
                  maximize=profit
                  )

    return model 

def get_model():
    units  = [4,3,2]
    values = [15,10,7]
    max_val = 9
    return smugglers_knapsack2(units,values,max_val)
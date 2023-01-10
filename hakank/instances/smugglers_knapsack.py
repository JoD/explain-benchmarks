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
# "Direct" approach
#
def smugglers_knapsack1():

    max_val = 9

    x = intvar(0,9,shape=3,name="x")
    whisky,perfume,cigarettes = x
    profit = intvar(0,1000,name="profit")
    
    #       Unit       Profit
    # Whisky:     4 units    15 dollars
    # Perfume:    3 units    10 dollars
    # Cigarettes: 2 units     7 dollars

    
    model = Model([4*whisky  + 3*perfume  + 2*cigarettes <= max_val, # Units
                   15*whisky + 10*perfume + 7*cigarettes == profit
                  ])

    model.maximize(profit)

    return model


def get_model():
    return smugglers_knapsack1()
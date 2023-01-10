"""
SEND+MOST=MONEY in CPMpy

Show all solutions with the maximum value of MONEY.
  
Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my CPMpy page: http://www.hakank.org/cpmpy/
"""
from cpmpy import *
import numpy
from instances.cpmpy_hakank import *
import copy

# Using solve and solveAll
def send_most_money3():
    
    x = intvar(0,9,shape=8)
    s,e,n,d,m,o,t,y = x
    money = intvar(0,99999)

    model = Model([money == 10000*m + 1000*o + 100*n + 10*e + y,
                   (s*1000 + e*100 + n*10 + d) + (m*1000 + o*100 + s*10 + t) == money,
                   s > 0,m > 0,
                   AllDifferent(x)
                   ])

    # Make an optimization model
    model2 = copy.copy(model)
    model2.maximize(money)

    MONEY = None
    ss = CPM_ortools(model2)
    ss.solve()
    if ss.solve():
        MONEY = money.value()

    # Find all optimal solutions
    model += money == MONEY


    return model

def get_model():
  return send_most_money3()

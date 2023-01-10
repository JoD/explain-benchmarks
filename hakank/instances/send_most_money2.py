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


# Another approach to get all (2) optimal values
# and don't have to do two calls to the model.
#
def send_most_money2():
    
    x = intvar(0,9,shape=8)
    s,e,n,d,m,o,t,y = x
    money = intvar(0,99999)

    model = Model([money == 10000*m + 1000*o + 100*n + 10*e + y,
                   (s*1000 + e*100 + n*10 + d) + (m*1000 + o*100 + s*10 + t) == money,
                   s > 0,m > 0,
                   AllDifferent(x)
                   ])
    model.maximize(money)

    MONEY = None
    ss = CPM_ortools(model)
    num_solutions = 0
    while ss.solve() is not False:
        num_solutions += 1
        print(x.value(), "money:",money.value() )        
        if MONEY == None:
            MONEY = money.value()
            ss += [money == MONEY]
        ss += any(x != x.value())
    print("num_solutions:",num_solutions)
    return model

def get_model():
  return send_most_money2()

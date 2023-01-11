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

def send_most_money(MONEY=None):
    x = intvar(0,9,shape=8)
    s,e,n,d,m,o,t,y = x
    money = intvar(0,99999)

    constraints = [money == 10000*m + 1000*o + 100*n + 10*e + y,
                   (s*1000 + e*100 + n*10 + d) + (m*1000 + o*100 + s*10 + t) == money,
                   s > 0,m > 0,
                   AllDifferent(x)]

    
    model = Model(constraints, maximize=money)
        
    return model

def get_model(seed=0):
  return send_most_money()
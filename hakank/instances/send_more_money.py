"""
SEND+MORE=MONEY in CPMpy

This is a different - and IMHO more natural - approach 
than the one in examples/send_more_money.py .

And in send_more_money2() there is a variant using scalar products.

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my CPMpy page: http://www.hakank.org/cpmpy/
"""
from cpmpy import *
import numpy as np
from instances.cpmpy_hakank import *

#
# "Plain algebraic" approach
#
def send_more_money():
    #print("send_more_money")
    x = IntVar(0,9,shape=8)
    s,e,n,d,m,o,r,y = x
    constraints = [    (s*1000 + e*100 + n*10 + d) 
                     + (m*1000 + o*100 + r*10 + e) 
                    == (10000*m + 1000*o + 100*n + 10*e + y),
                  s > 0,m > 0,
                  AllDifferent(x)
                 ]
    
    model = Model(constraints)
    return model

def get_model():
  return send_more_money()


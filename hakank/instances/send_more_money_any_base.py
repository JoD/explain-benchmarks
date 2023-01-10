"""
Send more money in any base problem in cpmpy.

Send More Money
   SEND
 + MORE
 ------
  MONEY

using any base.

Examples:
   Base 10 has one solution:
        {9, 5, 6, 7, 1, 0, 8, 2}
   Base 11 has three soltutions:
	{10, 5, 6, 8, 1, 0, 9, 2}
	{10, 6, 7, 8, 1, 0, 9, 3}
	{10, 7, 8, 6, 1, 0, 9, 2}
      

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my CPMpy page: http://www.hakank.org/cpmpy/
"""
from cpmpy import *
from cpmpy.solvers import *
import numpy as np
from instances.cpmpy_hakank import *




def send_more_money_any_base(base=10,num_sols=0,num_procs=1):
    x = intvar(0,base-1,shape=8,name="x")
    s,e,n,d,m,o,r,y = x
    model = Model([
                              s*base**3 + e*base**2 + n*base + d +
                              m*base**3 + o*base**2 + r*base + e ==
                  m*base**4 + o*base**3 + n*base**2 + e*base + y,
                  s > 0,
                  m > 0,
                  AllDifferent((s,e,n,d,m,o,r,y))
                  ]
                  )

    xs = [s,e,n,d, 
          m,o,r,e, 
          m,o,n,e,y]

    return model

def get_model(seed=0):
    import random
    random.seed(seed)
    b = int(random.uniform(10, 30))
    return send_more_money_any_base(b)
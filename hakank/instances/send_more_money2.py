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
from cpmpy_hakank import *

#
# Using scalar product
#
def send_more_money2():
    print("\nsend_more_money2 (prove unicity)")
    x = IntVar(0,9,shape=8)
    s,e,n,d,m,o,r,y = x
    send = IntVar(0,9999)
    more = IntVar(0,9999)
    money = IntVar(0,99999)        
    model = Model([s > 0,m > 0,
                   AllDifferent(x)
                   ]
                  )

    #
    # Some different ways to calculate the scalar product:
    #
    # base4 = base_array(4)
    # base5 = base_array(5)
    # model += [np.dot(base4,[s,e,n,d]) == send]
    # model += [np.dot(base4,[m,o,r,e]) == more]
    # model += [np.dot(base5,[m,o,n,e,y]) == money]
    
    # model += [sum(base4*[s,e,n,d]) == send]
    # model += [sum(base4*[m,o,r,e]) == more]
    # model += [sum(base5*[m,o,n,e,y]) == money]
    
    # model += [scalar_product(base4,[s,e,n,d]) == send]
    # model += [scalar_product(base4,[m,o,r,e]) == more]
    # model += [scalar_product(base5,[m,o,n,e,y]) == money]
    
    model += [scalar_product1([s,e,n,d]) == send]
    model += [scalar_product1([m,o,r,e]) == more]
    model += [scalar_product1([m,o,n,e,y]) == money]
    
    model += [send + more == money]

    return model

def get_model():
  return send_more_money2()

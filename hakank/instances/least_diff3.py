"""
Least diff problem in cpmpyy.

The model solves the following problem:
 
 What is the smallest difference between two numbers X - Y
 if you must use all the digits (0..9) exactly once, i.e.
 minimize the difference ABCDE - FGHIJ.


Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
from cpmpy import *
import numpy as np
from cpmpy_hakank import *

# Another approach
def least_diff3():
   x = IntVar(0,9, shape=10,name="x")
   a,b,c,d,e,f,g,h,i,j = x
   res                 = IntVar(0,200000,name="res")
    
   model = Model(minimize=res)
   model += [ AllDifferent(x) ]
   # model += [ res == sum([a,b,c,d,e] * np.flip(10**np.arange(5))) -
   #                   sum([f,g,h,i,j] * np.flip(10**np.arange(5)))]
   model += [ res == scalar_product1([a,b,c,d,e]) -
                     scalar_product1([f,g,h,i,j])]
   model += [ a > 0, f > 0, res > 0 ]

   return model


print("\nv3:")
def get_model():
    return least_diff3()


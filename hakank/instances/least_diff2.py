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
from instances.cpmpy_hakank import *

# This is Tias' version
def least_diff2():
   # Vars
   x = IntVar(0,9, shape=10,name="x")
   a,b,c,d,e,f,g,h,i,j = x
   res                 = IntVar(0,200000,name="res")

   model = Model([
       AllDifferent(x),       
       res == (a*10000 + b*1000 + c*100 + d*10 + e) - (f*10000 + g*1000 + h*100 + i*10 + j),
       a > 0,
       f > 0,
       res > 0,
   ],minimize=res)
   ss = CPM_ortools(model)

def get_model(seed=0):
    return least_diff2()



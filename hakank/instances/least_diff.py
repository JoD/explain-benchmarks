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

#
# Version 1
#
def least_diff1():

    x = IntVar(0,9, shape=10,name="x")
    a,b,c,d,e,f,g,h,i,j = x
    res                 = IntVar(0,200000,name="res")

    model = Model(minimize=res)
    model += [AllDifferent(x)]    
    model += [res == (a*10000 + b*1000 + c*100 + d*10 + e) - (f*10000 + g*1000 + h*100 + i*10 + j)]
    model += [a > 0,f > 0, res > 0]

    return model

def get_model():
    return least_diff1()

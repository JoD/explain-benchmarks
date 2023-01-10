"""
Simple integer programming problem (Chess set) in cpmpy.

From Applications of Optimization with XPress-MP.pdf
page 11. The problem is presented on page 7.


Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys, math,string
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *



def chess_set():
    small_set = intvar(0,100,name="small_set")
    large_set = intvar(0,100,name="large_set")
    z         = intvar(0,10000,name="z")
        
    model = Model([1*small_set + 3*large_set <= 200,
                   3*small_set + 2*large_set <= 160,
                   z == 5*small_set + 20*large_set,
                   ])


    model.maximize(z)

    return model

def get_model():
    return chess_set()

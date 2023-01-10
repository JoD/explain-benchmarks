"""
Simple regular expression in Google CP Solver.

My last name (Kjellerstrand) is quite often misspelled
in ways that this regular expression shows:
    k(je|ä)ll(er|ar)?(st|b)r?an?d

This model generates all the words that can be construed
by this regular expression.

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from cpmpy_hakank import *


def regexp_test(n):
    
    model = Model()

    #
    # data
    #
    # the DFA (for regular)
    n_states = 11
    input_max = 12
    initial_state = 1 # 0 is for the failing state
    accepting_states = [12]

    # The DFA
    transition_fn =  [
       # 1 2 3 4 5 6 7 8 9 0 1 2     # 
        [0,2,3,0,0,0,0,0,0,0,0,0],   #  1 k 
        [0,0,0,4,0,0,0,0,0,0,0,0],   #  2 je
        [0,0,0,4,0,0,0,0,0,0,0,0],   #  3 ä
        [0,0,0,0,5,6,7,8,0,0,0,0],   #  4 ll
        [0,0,0,0,0,0,7,8,0,0,0,0],   #  5 er
        [0,0,0,0,0,0,7,8,0,0,0,0],   #  6 ar
        [0,0,0,0,0,0,0,0,9,10,0,0],  #  7 st 
        [0,0,0,0,0,0,0,0,9,10,0,0],  #  8 b
        [0,0,0,0,0,0,0,0,0,10,0,0],  #  9 r
        [0,0,0,0,0,0,0,0,0,0,11,12], # 10 a
        [0,0,0,0,0,0,0,0,0,0,0,12],  # 11 n
                                     # 12 d 
        ]

    s = ['k','je','ä','ll','er','ar','st','b','r','a','n','d']
    # print('n:', n)

    #
    # declare variables
    #

    x = intvar(1,12,shape=n,name="x")

    #
    # constraints
    #
    model += [regular(x, n_states, input_max, transition_fn,
                      initial_state, accepting_states)]

    return model

def get_model(seed=0):
    import random
    random.seed(seed)
    n = int(random.uniform(4, 9))
    return regexp_test(n)

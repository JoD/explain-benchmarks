"""
Global constraint among_seq in cpmpy.

From Global constraint catalog:
http://www.emn.fr/x-info/sdemasse/gccat/Camong_seq.html
'''
Constraint

  among_seq(LOW,UP,SEQ,VARIABLES,VALUES)

Purpose  
Constrains all sequences of SEQ consecutive variables of the collection 
VARIABLES to take at least LOW values in VALUES and at most UP values 
in VALUES.

Example
  (
  1,2,4,<9,2,4,5,5,7,2>,
  <0,2,4,6,8>
  )

The among_seq constraint holds since the different sequences of 4 
consecutive variables contains respectively 2, 2, 1 and 1 even numbers.
'''


Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *


def among_seq_test(xval=None):

    n = 7

    # The set as a list
    v = [0,2,4,6,8]

    # variables
    x = intvar(0,9,shape=n,name="x")

    low = intvar(0,n-1,name="low")
    high = intvar(0,n-1,name="high")

    # Note: seqlen cannot be a decision variable since
    #       it's used together with range (in this implementation)
    # seqlen = intvar(1,n-1,name="seqlen")
    
    # low = 1
    # high = 2
    seqlen = 4

    # constraints

    if xval == None:
        model = Model([AllDifferent(x),
                       increasing(x),
                       among_seq(low,high,seqlen,x,v),
                       low == 1,
                       high == 2,
                       ])

    else:
        model = Model([x == xval,
                       among_seq(low,high,seqlen,x,v),
                       ])
      
    return model

def get_model(seed=0):
  xval=[9,2,4,5,5,7,2]
  return among_seq_test(xval)

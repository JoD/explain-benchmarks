"""
Five statements problem in cpmpy.

From 
'Puzzle: Joyner' five statements'
http://strathmaths.wordpress.com/2012/10/17/puzzle-joyners-five-statements/
'''
The following little logical teaser appears as 'Ponderable 1.1.3' in 
David Joyner's book Adventures in Group Theory (Johns Hopkins University 
Press, 2008; also available to download for free).

Determine which of the following statements is true.

 - Exactly one of these statements is false.
 - Exactly two of these statements are false.
 - Exactly three of these statements are false.
 - Exactly four of these statements are false.
 - Exactly five of these statements are false.

(Enthusiasts might like to consider the 'natural' generalisation to n statements, 
and in particular the case n=1..) Thanks to Dr André Sonnet for pointing this 
one out to me!
'''


Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys,math
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from cpmpy_hakank import *
from itertools import combinations

def five_statements(n=5):

    print("n:",n)
    x = boolvar(shape=(n,),name="x")

    model = Model()
    for i in range(n):
        model += [(x[i])==(sum([x[j] == 0 for j in range(n) ]) == i+1) ]

    return model

def get_model():
    return five_statements()

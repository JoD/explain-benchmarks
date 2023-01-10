"""
Perfect square sequence in cpmpy.

From 'Fun with num3ers'
'Sequence'
http://benvitale-funwithnum3ers.blogspot.com/2010/11/sequence.html
'''
If we take the numbers from 1 to 15 
    (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15) 
and rearrange them in such an order that any two consecutive 
numbers in the sequence add up to a perfect square, we get,

8     1     15     10     6     3     13     12      4      5     11     14        2      7      9
    9    16    25     16     9     16     25     16     9     16     25     16       9     16


I ask the readers the following:

Can you take the numbers from 1 to 25 to produce such an arrangement?
How about the numbers from 1 to 100?
'''


Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from cpmpy_hakank import *


def is_square(v):
    ub = v.ub # int(math.sqrt(v.Max()))
    z = intvar(1, ub)
    return [z*z == v]

def perfect_square_sequence(n=15, print_solutions=True, show_num_sols=0):

    model = Model()

    # create the table of possible squares
    squares = []
    for i in range(1, int(math.sqrt(n*n))):
        squares.append(i*i)
    # print("squares:", squares, len(squares))


    # declare variables
    x = intvar(1,n,shape=n,name="x")
    
    # constraints
    model += (AllDifferent(x))
    for i in range(1, n):
        model += (member_of(squares,x[i-1]+x[i]))


    return model

def get_model(seed=0):
    
    import random
    random.seed(seed)
    i = int(round(random.uniform(2, 100)))
    return perfect_square_sequence(i, False, 0)

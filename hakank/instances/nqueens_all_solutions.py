"""
N-queens problem in CPMpy

CSPlib prob054

Problem description from the numberjack example:
The N-Queens problem is the problem of placing N queens on an N x N chess
board such that no two queens are attacking each other. A queen is attacking
another if it they are on the same row, same column, or same diagonal.

Here are some different approaches with different version of both
the constraints and how to solve and print all solutions.


This CPMpy model was written by Hakan Kjellerstrand (hakank@gmail.com)
See also my CPMpy page: http://hakank.org/cpmpy/

"""
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *


def nqueens_v3(n=8,num_sols=0):

    queens = IntVar(1,n, shape=n)

    # Constraints on columns and left/right diagonal
    model = Model([
        AllDifferent(queens),
        AllDifferent([queens[i] - i for i in range(n)]),
        AllDifferent([queens[i] + i for i in range(n)]),
    ])

    # all solution solving, with blocking clauses
    return model
 
def get_model(seed=0):
    import random
    random.seed(seed)
    nqueens = int(round(random.uniform(8,30)))
    return nqueens_v3(n=nqueens)

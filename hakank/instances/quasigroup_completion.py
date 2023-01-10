"""
Quasigroup completion in cpmpy.

See Carla P. Gomes and David Shmoys:
'Completing Quasigroups or Latin Squares: Structured Graph Coloring Problem'

See also
Ivars Peterson 'Completing Latin Squares'
http://www.maa.org/mathland/mathtrek_5_8_00.html
'''
Using only the numbers 1, 2, 3, and 4, arrange four sets of these numbers into 
a four-by-four array so that no column or row contains the same two numbers. 
The result is known as a Latin square.
...
The so-called quasigroup completion problem concerns a table that is correctly 
but only partially filled in. The question is whether the remaining blanks in 
the table can be filled in to obtain a complete Latin square (or a proper 
quasigroup multiplication table).

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/
"""

import sys
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from cpmpy_hakank import *



default_n = 5
X = 0

# default problem
# (This is the same as quasigroup1.txt)
default_puzzle = [
    [1, X, X, X, 4],
    [X, 5, X, X, X],
    [4, X, X, 2, X],
    [X, 4, X, X, X],
    [X, X, 5, X, 1]
    ]


def quasigroup_completion(puzzle="",n=0,num_sols=0,num_procs=1):

    if puzzle == "":
        puzzle = default_puzzle
        n = default_n

    # Decision variables
    x = intvar(1,n,shape=(n,n),name="x")
    x_flat = x.flat

    model = Model()

    # Set the clues
    for i in range(0,n):
        for j in range(0,n):
            if puzzle[i][j] > X:
                model += [x[i,j] == puzzle[i][j]]

    # Rows and columns must be different
    model += [
        [AllDifferent(row) for row in x],
        [AllDifferent(col) for col in x.transpose()]
        ]

    return model


#
# Read a problem instance from a file
#
def read_problem(file):
    f = open(file, 'r')
    n = int(f.readline())
    game = []
    for i in range(n):
        x = f.readline()
        row_x = (x.rstrip()).split(" ")
        row = [0]*n
        for j in range(n):
            if row_x[j] == ".":
                tmp = 0
            else:
                tmp = int(row_x[j])
            row[j] = tmp
        game.append(row)
    return [game, n]

def get_model(seed=0):
    import random
    random.seed(seed)
    p = int(round(random.uniform(1, 9)))
    
    [game, n] = read_problem("quasigroup" +str(p) + ".txt")
    return quasigroup_completion(game, n)
"""
Survo puzzle in cpmpy.

http://en.wikipedia.org/wiki/Survo_Puzzle
'''
Survo puzzle is a kind of logic puzzle presented (in April 2006) and studied 
by Seppo Mustonen. The name of the puzzle is associated to Mustonen's 
Survo system which is a general environment for statistical computing and 
related areas.

In a Survo puzzle the task is to fill an m * n table by integers 1,2,...,m*n so 
that each of these numbers appears only once and their row and column sums are 
equal to integers given on the bottom and the right side of the table. 
Often some of the integers are given readily in the table in order to 
guarantee uniqueness of the solution and/or for making the task easier.
'''

See also
http://www.survo.fi/english/index.html
http://www.survo.fi/puzzles/index.html

References:
* Mustonen, S. (2006b). 'On certain cross sum puzzles'
  http://www.survo.fi/papers/puzzles.pdf 
* Mustonen, S. (2007b). 'Enumeration of uniquely solvable open Survo puzzles.' 
  http://www.survo.fi/papers/enum_survo_puzzles.pdf 
* Kimmo Vehkalahti: 'Some comments on magic squares and Survo puzzles' 
  http://www.helsinki.fi/~kvehkala/Kimmo_Vehkalahti_Windsor.pdf
* R code: http://koti.mbnet.fi/tuimala/tiedostot/survo.R

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my CPMpy page: http://www.hakank.org/cpmpy/

"""
import sys
from cpmpy import *
import numpy as np
from instances.cpmpy_hakank import *
import random

#
# Read a problem instance from a file
#
def read_problem(file):
    f = open(file, 'r')
    r = int(f.readline())
    c = int(f.readline())
    rowsums = f.readline()
    colsums = f.readline()
    rowsums = [int(t) for t in (rowsums.rstrip()).split(",")]
    colsums = [int(t) for t in (colsums.rstrip()).split(",")]
    game = []
    for i in range(r):
        x = f.readline()
        x = [int(t) for t in (x.rstrip()).split(",")]
        row = [0]*c
        for j in range(c):
            row[j] = int(x[j])
        game.append(row)
    return [r, c, rowsums, colsums, game]


def survo_puzzle(r=0, c=0, rowsums=[], colsums=[], game=[]):

    if r == 0:
        r = 3
        c = 4
        rowsums = [30,18,30]
        colsums = [27,16,10,25]
        game = [[0, 6, 0, 0],
                [8, 0, 0, 0],
                [0, 0, 3, 0]]

    x = intvar(1,r*c,shape=(r,c),name="x")

    model = Model(
                   AllDifferent(x),
                   [rowsums[i] == sum([x[i][j] for j in range(c)]) for i in range(r)],
                   [colsums[j] == sum([x[i][j] for i in range(r)]) for j in range(c)]
                 )
    # copy game matrix
    for i in range(r):
      for j in range(c):
          if game[i][j] > 0:
              model += [x[i,j] == game[i][j]]

    return model


def get_model(seed=0):
    import os
    base_path = os.path.realpath(__file__).replace('survo_puzzle.py', '')
    files = [
        "survo_puzzle1.txt",
        "survo_puzzle2.txt",
        "survo_puzzle3.txt",
        "survo_puzzle4.txt",
        "survo_puzzle5.txt",
        "survo_puzzle6.txt",
    ]
    random.seed(seed)
    p = random.choice(files)
    r, c, rowsums, colsums, game = read_problem(base_path + p)
    return survo_puzzle(r, c, rowsums, colsums, game)


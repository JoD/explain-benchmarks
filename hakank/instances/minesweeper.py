"""
Minesweeper problem in cpmpy.

From gecode/examples/minesweeper.cc:
'''
A specification is a square matrix of characters. Alphanumeric 
characters represent the number of mines adjacent to that field. 
Dots represent fields with an unknown number of mines adjacent to 
it (or an actual mine).
'''

E.g.
     "..2.3."
     "2....."
     "..24.3"
     "1.34.."
     ".....3"
     ".3.3.."

Also see 
* http://www.janko.at/Raetsel/Minesweeper/index.htm
* http://en.wikipedia.org/wiki/Minesweeper_(computer_game)
* Ian Stewart on Minesweeper: http://www.claymath.org/Popular_Lectures/Minesweeper/
* Richard Kaye's Minesweeper Pages
  http://web.mat.bham.ac.uk/R.W.Kaye/minesw/minesw.htm
  * Richard Kaye: "Some Minesweeper Configurations"
  http://web.mat.bham.ac.uk/R.W.Kaye/minesw/minesw.pdf

Most instances has one or just a few solutions.
The exception is minesweeper_kaye_splitter.txt
which has a lot of solutions (131072).


Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from cpmpy_hakank import *



#
# Default problem from "Some Minesweeper Configurations",page 3
# (same as problem instance minesweeper_config3.txt)
# It has 4 solutions
# 
X = -1
default_game = [
            [2,3,X,2,2,X,2,1],
            [X,X,4,X,X,4,X,2],
            [X,X,X,X,X,X,4,X],
            [X,5,X,6,X,X,X,2],
            [2,X,X,X,5,5,X,2],
            [1,3,4,X,X,X,4,X],
            [0,1,X,4,X,X,X,3],
            [0,1,2,X,2,3,X,2]
            ]
default_r = 8
default_c = 8


#
# Solve the Minesweeper problem
#
def minesweeper(game="", r="", c=""):

    # Set default problem
    if game == "":
        game = default_game
        r = default_r
        c = default_c

    #
    # Decision variables
    mines = intvar(0,1,shape=(r,c),name="mines")
    S = [-1,0,1]  # for the neighbors of this cell

    model = Model()
    
    for i in range(r):
        for j in range(c):
            if game[i][j] >= 0:
                # This cell cannot be a mine
                model += [mines[i,j] == 0]
                
                # this cell is the sum of all the surrounding cells
                model += [
                    game[i][j] == sum([mines[i+a,j+b]
                                       for a in S for b in S
                                       if i+a>=0 and
                                          j+b>=0 and
                                          i+a<r  and
                                          j+b<c
                                       ])
                    ]

            else:
                model += [mines[i,j] >= 0]

    return model

#
# Read a problem instance from a file
#
def read_problem(file):
    f = open(file, 'r')
    rows = int(f.readline())
    cols = int(f.readline())
    game = []
    for i in range(rows):
        x = f.readline()
        row = [0]*cols
        for j in range(cols):
            if x[j] == ".":
                tmp = -1
            else:
                tmp = int(x[j])
            row[j] = tmp
        game.append(row)
    return [game, rows, cols]


# file = "minesweeper1.txt"
def get_model(seed=0):
    all_files = [
        "minesweeper0.txt", 
        "minesweeper1.txt", 
        "minesweeper2.txt", 
        "minesweeper3.txt", 
        "minesweeper4.txt", 
        "minesweeper5.txt", 
        "minesweeper6.txt", 
        "minesweeper7.txt", 
        "minesweeper8.txt", 
        "minesweeper9.txt", 
        "minesweeper_config2.txt", 
        "minesweeper_config3.txt", 
        "minesweeper_kaye_splitter.txt", 
        "minesweeper_kaye_wire.txt", 
        ]
    import random
    random.seed(seed)
    file = random.choice(all_files)
    [game, rows, cols] = read_problem(file)

    return minesweeper(game, rows, cols)    

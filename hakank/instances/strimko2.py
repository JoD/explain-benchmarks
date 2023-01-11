"""
Strimko problem in cpmpy.

From
360: A New Twist on Latin Squares
http://threesixty360.wordpress.com/2009/08/04/a-new-twist-on-latin-squares/
'''
The idea is simple: each row and column of an nxn grid must contain
the number 1, 2, ... n exactly once (that is, the grid must form a
Latin square), and each "stream" (connected path in the grid) must
also contain the numbers 1, 2, ..., n exactly once.
'''

For more information, see:
* http://www.strimko.com/
* http://www.strimko.com/rules.htm
* http://www.strimko.com/about.htm
* http://www.puzzlersparadise.com/Strimko.htm

I have blogged about this (using MiniZinc model) in
'Strimko - Latin squares puzzle with "streams"'
http://www.hakank.org/constraint_programming_blog/2009/08/strimko_latin_squares_puzzle_w_1.html

This cpmpy model was written by Hakan Kjellerstrand (hakank@gmail.com)
See also my cpmpy page: http://hakank.org/cpmpy/
  
"""
from cpmpy import *
import cpmpy.solvers
import numpy as np
from instances.cpmpy_hakank import *
import random
import instances.strimko2_002 as strimko2_002
import instances.strimko2_067 as strimko2_067
import instances.strimko2_068 as strimko2_068  
import instances.strimko2_069 as strimko2_069 
import instances.strimko2_070 as strimko2_070


def strimko2(streams='', placed=''):

  model = Model()

  #
  # default problem
  #
  if streams == '':
    streams = [[1, 1, 2, 2, 2, 2, 2], [1, 1, 2, 3, 3, 3, 2],
               [1, 4, 1, 3, 3, 5, 5], [4, 4, 3, 1, 3, 5, 5],
               [4, 6, 6, 6, 7, 7, 5], [6, 4, 6, 4, 5, 5, 7],
               [6, 6, 4, 7, 7, 7, 7]]

    # Note: This is 1-based
    placed = [[2, 1, 1], [2, 3, 7], [2, 5, 6], [2, 7, 4], [3, 2, 7], [3, 6, 1],
              [4, 1, 4], [4, 7, 5], [5, 2, 2], [5, 6, 6]]

  n = len(streams)
  num_placed = len(placed)

  #print('n:', n)

  # variables
  x = intvar(1,n,shape=(n,n), name="x")

  # constraints

  # all rows and columns must be unique, i.e. a Latin Square
  for i in range(n):
    row = [x[i, j] for j in range(n)]
    model += [AllDifferent(row)]

    col = [x[j, i] for j in range(n)]
    model += [AllDifferent(col)]

  #
  # streams
  #
  for s in range(1, n + 1):
    tmp = [x[i, j] for i in range(n) for j in range(n) if streams[i][j] == s]
    model += [AllDifferent(tmp)]

  #
  # placed
  #
  for i in range(num_placed):
    # note: also adjust to 0-based
    model += [x[placed[i][0] - 1, placed[i][1] - 1] == placed[i][2]]

  return model

def get_model(seed=0):
  problem_files = {
    "strimko2_002":strimko2_002.get_instance,
    "strimko2_067":strimko2_067.get_instance,
    "strimko2_068":strimko2_068.get_instance,
    "strimko2_069":strimko2_069.get_instance,
    "strimko2_070":strimko2_070.get_instance
  }
  problem_file = random.choice(list(problem_files))
  streams, placed = problem_files[problem_file]()
  return strimko2(streams, placed)

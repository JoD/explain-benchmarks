"""
Rogo puzzle solver in cpmpy.

From http://www.rogopuzzle.co.nz/
'''
The object is to collect the biggest score possible using a given
number of steps in a loop around a grid. The best possible score
for a puzzle is given with it, so you can easily check that you have
solved the puzzle. Rogo puzzles can also include forbidden squares,
which must be avoided in your loop.
'''

Also see Mike Trick:
'Operations Research, Sudoko, Rogo, and Puzzles'
http://mat.tepper.cmu.edu/blog/?p=1302

Problem instances:
* http://www.hakank.org/cpmpy/rogo_mike_trick.py
* http://www.hakank.org/cpmpy/rogo_20110106.py
* http://www.hakank.org/cpmpy/rogo_20110107.py

Note: This model is currently not correct probably since abs() don't work as expected.

This cpmpy model was written by Hakan Kjellerstrand (hakank@gmail.com)
See also my cpmpy page: http://hakank.org/cpmpy/
  
"""
from cpmpy import *
import cpmpy.solvers
import numpy as np
from cpmpy_hakank import *


def rogo2(problem, rows, cols, max_steps):
  
  #
  # data
  #
  W = 0
  B = -1
  print("rows: %i cols: %i max_steps: %i" % (rows, cols, max_steps))
  print("Problem:")
  for p in problem:
    print(p)
    
  problem_flatten = [problem[i][j] for i in range(rows) for j in range(cols)]
  max_point = max(problem_flatten)
  print("max_point:", max_point)
  max_sum = sum(problem_flatten)
  print("max_sum:", max_sum)
  print()

  #
  # declare variables
  #

  # the coordinates
  x = intvar(0,rows-1,shape=max_steps,name="x")
  y = intvar(0,cols-1,shape=max_steps,name="y")  

  # the collected points
  points = intvar(0,max_point,shape=max_steps,name="points")
  
  # objective: sum of points in the path
  sum_points = intvar(0, max_sum,name="sum_points")

  # objective
  model = Model(maximize=sum_points)
  
  # constraints

  # all coordinates must be unique
  for s in range(max_steps):
    for t in range(s + 1, max_steps):
      b1 = x[s] != x[t]
      b2 = y[s] != y[t]
      model += (b1 + b2 >= 1)

  # calculate the points (to maximize)
  for s in range(max_steps):
    model += (points[s] == Element(problem_flatten, x[s]*cols + y[s]))

  model += (sum_points == sum(points))

  # ensure that there are no black cells in the path
  for s in range(max_steps):
    model += (Element(problem_flatten, x[s]*cols + y[s]) != B)

  # get the path
  for s in range(max_steps - 1):
    model += (abs(x[s] - x[s + 1]) + abs(y[s] - y[s + 1]) == 1)

  # close the path around the corner
  model += (abs(x[max_steps - 1] - x[0]) + abs(y[max_steps - 1] - y[0]) == 1)

  # symmetry breaking: the cell with lowest coordinates
  # should be in the first step.
  for i in range(1, max_steps):
    model += (x[0] * cols + y[0] < x[i] * cols + y[i])

  # symmetry breaking: second step is larger than first step
  model += (x[0]*cols+y[0] < x[1]*cols+y[1])

  return model


def get_model():
  # Default problem:
  # Data from
  # Mike Trick: "Operations Research, Sudoko, Rogo, and Puzzles"
  # http://mat.tepper.cmu.edu/blog/?p=1302
  #
  # This has 48 solutions with symmetries;
  # 4 when the path symmetry is removed.
  #
  rows = 5
  cols = 9
  max_steps = 12
  W = 0
  B = -1
  problem = [[2, W, W, W, W, W, W, W, W], [W, 3, W, W, 1, W, W, 2, W],
            [W, W, W, W, W, W, B, W, 2], [W, W, 2, B, W, W, W, W, W],
            [W, W, W, W, 2, W, W, 1, W]]

  return rogo2(problem, rows, cols, max_steps)


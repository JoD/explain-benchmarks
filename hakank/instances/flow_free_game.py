"""
Flow Free game in cpmpy.

https://www.bigduckgames.com/flowfree
'''
Flow Free® is a simple yet addictive puzzle game.

Connect matching colors with pipe to create a Flow®. Pair all colors, and cover the
entire board to solve each puzzle in Flow Free. But watch out, pipes will break if
they cross or overlap!
'''

This is a port of the z3 model (by commenter JohanC) in
https://stackoverflow.com/questions/67412516/how-to-solve-flow-game-using-google-or-tools

Note: This will show images (via matplotlib) for two instances. Close the window
of the first windo to see the next solution.

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my CPMpy page: http://www.hakank.org/cpmpy/

"""
from cpmpy import *
import numpy as np
from instances.cpmpy_hakank import *
import matplotlib.pyplot as plt


def flow_free(board):
  M = len(board)
  N = len(board[0])
  B = intvar(1,10,shape=(N,M), name="B")

  model = Model()

  for i in range(M):
    for j in range(N):
      same_neighs_ij = sum([B[i][j] == B[k][l] 
                            for k in range(M) for l in range(N) if abs(k - i) + abs(l - j) == 1])
      if board[i][j] != 0:
        model += [B[i,j] == board[i][j]]
        model += [same_neighs_ij == 1]
      else:
        model += [(same_neighs_ij == 2) | (B[i][j] == 0)]

  return model
  
def get_model(seed=0):
  board1 = [[1, 0, 0, 2, 3],
            [0, 0, 0, 4, 0],
            [0, 0, 4, 0, 0],
            [0, 2, 3, 0, 5],
            [0, 1, 5, 0, 0]]

  # Another instance
  board2 = [[0, 1, 2, 0, 0, 0, 0],
            [1, 3, 4, 0, 3, 5, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 4, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 5, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]]
  import random
  random.seed(seed)
  board = random.choice([board1, board2])

  return flow_free(board)

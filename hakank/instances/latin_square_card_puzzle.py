"""
Latin square card puzzle (Graeco-Latin_square) in cpmpy.

Problem from Mario Livio's book about group theory
'The Equation that couldn't be solved',
page 22
'''
... Incidentally, you may get a kick out of solving this
eighteenth century card puzzle: Arrange all the jacks,
queens, kings, and aces from a deck of cards in a square so that 
no suit or value would appear twice in any row, column, or the
two main diagonals.
'''

Also see
- http://en.wikipedia.org/wiki/Graeco-Latin_square
- http://en.wikipedia.org/wiki/Thirty-six_officers_problem

Note: This model generalize the problem to use values of 0..n-1
instead of jacks, queens, kings, and aces, as well as 0..n-1
instead of the suits.

For n=4:

  * Without symmetry breaking, there are 1156 solutions

  * With symmetry breaking there are two solutions:
  
    0/0 1/1 2/2 3/3 
    3/2 2/3 1/0 0/1 
    1/3 0/2 3/1 2/0 
    2/1 3/0 0/3 1/2 


    0/0 1/1 2/2 3/3 
    2/3 3/2 0/1 1/0 
    3/1 2/0 1/3 0/2 
    1/2 0/3 3/0 2/1 


    Or in the original formulation using cards:


    J/H Q/S K/C A/D 
    A/C K/D Q/H J/S 
    Q/D J/C A/S K/H 
    K/S A/H J/D Q/C 


    J/H Q/S K/C A/D 
    K/D A/C J/S Q/H 
    A/S K/H Q/D J/C 
    Q/C J/D A/H K/S 


As Euler realized there is no solution for n=6.
Our model realizes this in 0.17s.

From http://en.wikipedia.org/wiki/Graeco-Latin_square
'''
No group based Graeco-Latin squares can exist if the order is an odd multiple of two
(that is, equal to 4k + 2 for some positive integer k).[3]
'''

Example of n without solutions: [4*k + 2 for k in range(10)]
[2, 6, 10, 14, 18, 22, 26, 30, 34, 38]


Here are some solutions for n > 4

n:7, 1 solution(s), timeout:120s
0/0 1/1 2/2 3/3 4/4 5/5 6/6 
5/6 6/2 1/3 2/4 3/5 4/0 0/1 
1/4 3/0 4/6 5/1 0/2 6/3 2/5 
4/1 0/3 6/4 1/5 2/0 3/6 5/2 
6/5 2/6 3/1 4/2 5/3 0/4 1/0 
3/2 5/4 0/5 6/0 1/6 2/1 4/3 
2/3 4/5 5/0 0/6 6/1 1/2 3/4 

ExitStatus.FEASIBLE (1.433043319 seconds)
Nr solutions: 1
Num conflicts: 7511
NumBranches: 15810
WallTime: 1.433043319


n:8, 1 solution(s), timeout:120s
0/0 1/1 2/2 3/3 4/4 5/5 6/6 7/7 
3/6 6/7 0/3 4/0 7/5 1/2 5/1 2/4 
6/1 7/4 4/6 5/2 1/3 2/0 3/7 0/5 
5/7 2/6 7/0 1/5 3/2 6/3 0/4 4/1 
7/3 3/5 5/4 0/6 2/1 4/7 1/0 6/2 
4/2 5/0 6/5 7/1 0/7 3/4 2/3 1/6 
2/5 4/3 1/7 6/4 5/6 0/1 7/2 3/0 
1/4 0/2 3/1 2/7 6/0 7/6 4/5 5/3 

ExitStatus.FEASIBLE (37.510059891000004 seconds)
Nr solutions: 1
Num conflicts: 179851
NumBranches: 527762
WallTime: 37.510059891000004


Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys,math
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *
import time


def latin_square_card_puzzle(n=4,symmetry_breaking=True,num_sols=1,timeout=None,as_original=False):

  m = math.ceil((n*(n+1)) / 2)
  # the values of the n*n cards, e.g. for n=4:
  #  [0, 10, 20, 30, 1, 11, 21, 31, 2, 12, 22, 32, 3, 13, 23, 33]
  cards = [i + m*j for i in range(n) for j in range(n)]
  min_card = min(cards)
  max_card = max(cards)
  
  # decision variables
  x = intvar(min_card,max_card,shape=(n,n),name="x")
  x_flat = [x[i,j] for i in range(n) for j in range(n)]
  
  # accept only the values in cards
  model = Model([x[i,j] != c for i in range(n) for j in range(n)
                 for c in range(min_card,max_card) if not c in cards])

  model += [AllDifferent(x),

            # diagonals1
            AllDifferent([x[i,i] / m for i in range(n) ]),
            AllDifferent([x[i,i] % m for i in range(n) ]),

            # diagonal2
            AllDifferent([x[i,n-i-1] / m for i in range(n) ]),
            AllDifferent([x[i,n-i-1] % m for i in range(n) ])
            ]

  # rows, columns, 
  for i in range(n):
      model += [AllDifferent([x[i,j] / m for j in range(n) ]),
                AllDifferent([x[j,i] / m for j in range(n) ]),
            
                AllDifferent([x[i,j] % m for j in range(n) ]),
                AllDifferent([x[j,i] % m for j in range(n) ])
                ]
                
  # Symmetry breaking
  if symmetry_breaking:
      model += [x[0,0] == 0,
                increasing([x[0,j] / m for j in range(n)]),
                increasing([x[0,j] % m for j in range(n)]),
                ]

  return model

def get_model(seed=0):
  
  symmetry_breaking=True
  import random
  random.seed(seed)
  n = int(round(random.uniform(2, 9)))

  return latin_square_card_puzzle(n,symmetry_breaking)
    

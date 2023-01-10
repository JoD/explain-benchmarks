"""
  Consecutive integer partition problem in CPMpy.

  From  Tadao Kitzawa 'Arithmetical, Geometrical and Combinatorial Puzzles from Japan', 
  problem 2, page 1
  '''
  Problem 2
  The consecutive integers from 1 to n are partitioned into several groups such
  that in each group, the largest number is equal to the sum of the remaining
  numbers.
  (a) How many groups are there if n = 12?
  (b) What are the numbers of groups that may work if n = 14?
  '''

  See more discussion and experiments of this problem in 
  Also see http://hakank.org/picat/consecutive_integer_partition_problem.pi

  Note: Here I don't assume anything about the sizes of the groups, except
  that a group must have at least three values, otherwise there can be no 
  maximum value and remainder numbers that adds to the maximum number. 
  There can, for example, be groups with different number of elements:
  for n = 12 all groups are of size 3 but for n=16 there are groups of 
  size 3 and of size 4.


  a) For n = 12, the number of groups are 4
     Without symmetry breaking, there are 192 different solutions.
     With symmetry breaking (see the model), there are only these 3 solutions:
     
       n: 12 m: 4
       sol #1
       [0 1 2 3 1 2 1 3 2 0 0 3]
       [11  7  9 12]

       sol #2
       [0 1 2 3 0 0 2 3 1 2 1 3]
       [ 6 11 10 12]
       
       sol #3
       [0 1 2 1 3 1 3 2 0 0 2 3]
       [10  6 11 12]
       
       ExitStatus.OPTIMAL (0.00836223 seconds)
       Nr solutions: 3
       Num conflicts: 98
       NumBranches: 153
       WallTime: 0.00836223


  b) For n = 14, there are no solutions.


  Number of solutions (with symmetry breaking):
   n: 3 m: 1 #sols: 1
   n: 12 m: 4 #sols: 3
   n: 15 m: 5 #sols: 8
   n: 16 m: 5 #sols: 31
   n: 19 m: 6 #sols: 215
   n: 20 m: 6 #sols: 530
   n: 23 m: 7 #sols: 4230
   n: 24 m: 8 #sols: 617
   n: 27 m: 9 #sols: 4378
   n: 28 m: 9 #sols: 58160


  Findings:
  - the number of groups is max([1,n // 3]) for those n that has a solution.
  - the instance is solvable for N=3 and if N mod 4 == 0 or N mod 4 == 3. 

  See more about this in the Picat model
  http://hakank.org/picat/consecutive_integer_partition_problem.pi  

  
Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys,time
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *

def consecutive_integers_problem(n=12,m=None,symmetry_breaking=True,num_sols=0,print_solutions=True):

    # decision variables
    x     = intvar(0,m-1,shape=(n,),name="x")
    maxes = intvar(m,n,shape=(m,),name="maxes")

    # constraints
    model = Model()
    for g in range(m):
        model += [atleast(x,g,3), # The group size must be at least 3 elements
                  maxes[g] == max([(j+1)*(x[j] == g) for j in range(n)]),
                  maxes[g] == (sum([(j+1)*(x[j] == g) for j in range(n)]) - maxes[g])
                  ]

    if symmetry_breaking:
        model += [value_precede_chain(range(m),x)]
        model += [maxes[m-1]==n]

    return model

# For N = 12 there are 3 solutions with symmetry breaking

def get_model(seed=0):
  n=12
  
  import random
  random.seed(seed)
  m = random.choice(list(mi for mi in range(1,1+(n // 3))))

  return  consecutive_integers_problem(n, m)

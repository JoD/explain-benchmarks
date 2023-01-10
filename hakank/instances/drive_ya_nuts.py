"""
Drive Ya Nuts puzzle in cpmpy.

From http://www.samstoybox.com/toys/DriveYaNuts.html
'''
The Drive Ya Nuts puzzle by Milton Bradley was cool and quite difficult. The object of 
the puzzle is to place all seven nuts such that the numbers on all sides of each 
nut match the numbers on the adjoining nut. There is but one way to solve the puzzle. 
Here are two versions of puzzle. Note that the second one is still factory sealed and 
shows the solution. So you think it sounds easy? 
'''

Some other links: 
- http://www.jaapsch.net/puzzles/circus.htm

Representation:

A side of a nut is numbered as following

          1
      6       2
      5       3
          4


and the 7 nuts are numbered as follows:

           0 

       5       1
           6
       4        2

           3

i.e. nut 6 is the master (center) nut.

Note: There are 6 solutions, depending on how we orient
      the center nut (6). This is handled by symmetry breaking below.

Here is one solution (which has the center nut start with 1):

   2 3 5 1 4 6    Nut 0 (in the representation above)
   3 2 4 1 6 5    Nut 1
   1 4 3 6 5 2    Nut 2
   4 5 6 1 2 3    Nut 3
   2 5 3 1 6 4    Nut 4
   5 4 3 2 1 6    Nut 5
   1 6 2 4 5 3    Nut 6 (center nut)

E.g. the first nut is the nut 1,4,6,2,3,5 rotated like this, i.e.
with 2 at 12 o'clock and then clock wise: 2,3,5,1,4, and 6:
   
          2
      6       3
      4       5
          1

And so on with the other nuts.

Here is a complete solution for the first instance:

Solution:
nuts (in order)
[1 2 3 4 5 6] pos: 0 
[1 4 3 6 5 2] pos: 5 
[1 4 6 2 3 5] pos: 3 
[1 6 2 4 5 3] pos: 6 center nut
[1 6 4 2 5 3] pos: 1 
[1 6 5 3 2 4] pos: 4 
[1 6 5 4 3 2] pos: 2 

x:
[1 2 3 4 5 6]
[1 6 4 2 5 3]
[2 1 6 5 4 3]
[1 4 6 2 3 5]
[1 6 5 3 2 4]
[6 5 2 1 4 3]
[4 5 3 1 6 2]

                      1
                  6       2
                  5       3
                      4

    6                                   1
3       5                           3       6
4       2                           5       4
    1                                   2


                      4
                  2       5
                  6       3
                      1

    1                                   2
4       6                           3       1
2       5                           4       6
    3                                   5


                      1
                  5       4
                  3       6
                      2


Here we can see that for the top nut (nut 0) is connected:
* with nut 1 (up right) with the value 3
* with nut 6 (center)   with the value 4
* with nut 5 (up left)  with the value 5


[Comment from the MiniZinc model
 http://www.hakank.org/minizinc/drive_ya_nuts.mzn:
Note: I started with this MiniZinc model after reading the Frink 
implementation by Alan Eliasen 
    http://futureboy.us/fsp/colorize.fsp?f=DriveYaNuts.frink
which had the link cited above. The Frink program use a different 
approach, though.
]

Personal comment: 
This is the same puzzle as the infamous AWA-Patent problem 
from a long long time ago, though I didn't then know what 
it was called. My father got this problem from AWA-Patent (as a
Christmas gift?) as he was a member of a Swedish inventor
organization ('Svenska Uppfinnareforeningen').

Yes, I did solve it manually without any computational help.


Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my CPMpy page: http://www.hakank.org/cpmpy/

"""
import random
from cpmpy import *
import numpy as np
from cpmpy_hakank import *


def pp(v):
  return v.value()

def drive_ya_nuts(problem):
    
  m = 7 # Number of nuts 
  n = 6 # Side per nut
  n2 = n*2 # The full representation of a nut

  nuts = cpm_array(problem["nuts"]) 
  nuts_flat = [nuts[i,j] for i in range(m) for j in range(n2)]

  # The connection points between the nuts, i.e. where the values
  # must be the same.
  # (Not surprisingly there are some permutations involved.)
  #
  #                       nuts    sides to be equal
  connections = np.array([[0,1,      2,5],  # nut[0,2] == nut[1,5]
                          [1,2,      3,0],  # ...
                          [2,3,      4,1],
                          [3,4,      5,2],
                          [4,5,      0,3],
                          [5,0,      1,4],
                          
                          [6,0,      0,3], # the center nut vs the other
                          [6,1,      1,4],
                          [6,2,      2,5],
                          [6,3,      3,0],
                          [6,4,      4,1],
                          [6,5,      5,2]])


  num_connections = len(connections)

  # variables

  # The nuts are numbered 1..n
  x = intvar(1,n,shape=(m,n),name="x")

  # Which nut is this? (in the nuts matrix)
  # The nuts are represented as 0..m-1
  pos = intvar(0,m-1,shape=m,name="pos") 

  # Permutation array of pos. For displaying the result.
  pos_inv = intvar(0,m-1, shape=m,name="pos_inv") 

  # indices to start the nut (in the nut's m x n*2 matrix)
  start_ix = intvar(0,n-1,shape=m,name="start_ix")

  # Constraints
  model = Model([AllDifferent(pos),
                 inverse(pos,pos_inv), # for display
                 ])

  for i in range(m):
    model += [AllDifferent(x[i])]

    # for some "rotation" of each nut...
    for j in range(n):
      # x[i,j] == nuts[p,j+k] # don't work
      model += [x[i,j] == Element(nuts_flat,pos[i]*n2 + start_ix[i]+j)]

  # check the connections
  for c in range(num_connections):
    cc = connections[c]
    model += [x[cc[0],cc[2]] == x[cc[1],cc[3]]]

  # symmetry breaking: 
  model += [start_ix[0] == 0]

  return model

#
# Problem instances.
#
# Note that these instances are really the same problem but has
# different orders of the nuts.
#

#
# The nuts are duplicated so we can use an offset in the array.
# They are arranged so that each nut starts with 1.
# 
def get_model(seed=0):
  drive_ya_nuts_problems = {

    # "arbitrary" order (sorted)
    # Note that pos_inv for the shown solution is the permutation 
    # [4,3,1,7,5,2,6]
    "problem1" : {
    "nuts" : [
      [1,2,3,4,5,6, 1,2,3,4,5,6], # 4 (row 4 in the solution order shown above)
      [1,4,3,6,5,2, 1,4,3,6,5,2], # 3
      [1,4,6,2,3,5, 1,4,6,2,3,5], # 1 
      [1,6,2,4,5,3, 1,6,2,4,5,3], # 7 [center nut]
      [1,6,4,2,5,3, 1,6,4,2,5,3], # 5
      [1,6,5,3,2,4, 1,6,5,3,2,4], # 2 
      [1,6,5,4,3,2, 1,6,5,4,3,2]  # 6 
      ]

    },
      

    #
    # This is the nuts in the solution order.
    #
    "problem2" : {
    "nuts": [[1,4,6,2,3,5, 1,4,6,2,3,5], # 1 
            [1,6,5,3,2,4, 1,6,5,3,2,4], # 2 
            [1,4,3,6,5,2, 1,4,3,6,5,2], # 3
            [1,2,3,4,5,6, 1,2,3,4,5,6], # 4
            [1,6,4,2,5,3, 1,6,4,2,5,3], # 5
            [1,6,5,4,3,2, 1,6,5,4,3,2], # 6 
            [1,6,2,4,5,3, 1,6,2,4,5,3]  # 7 # center nut
            ]
    },

    # Another order
    "problem3" : {
    "nuts" : [[1,6,5,3,2,4, 1,6,5,3,2,4], # 2 
              [1,2,3,4,5,6, 1,2,3,4,5,6], # 4 (row 4 in the solution order shown above)
              [1,6,2,4,5,3, 1,6,2,4,5,3], # 7 [center nut]
              [1,6,4,2,5,3, 1,6,4,2,5,3], # 5
              [1,6,5,4,3,2, 1,6,5,4,3,2], # 6 
              [1,4,6,2,3,5, 1,4,6,2,3,5], # 1 
              [1,4,3,6,5,2, 1,4,3,6,5,2]  # 3
              ]
    },

  }
  import random
  random.seed(seed)
  p = random.choice(list(drive_ya_nuts_problems))
  return drive_ya_nuts(drive_ya_nuts_problems[p])


"""
Sicherman Dice in cpmpy.

From http://en.wikipedia.org/wiki/Sicherman_dice
"" 
Sicherman dice are the only pair of 6-sided dice which are not normal dice, 
bear only positive integers, and have the same probability distribution for 
the sum as normal dice.

The faces on the dice are numbered 1, 2, 2, 3, 3, 4 and 1, 3, 4, 5, 6, 8.
""

I read about this problem in a book/column by Martin Gardner long
time ago, and got inspired to model it now by the WolframBlog post
'Sicherman Dice': http://blog.wolfram.com/2010/07/13/sicherman-dice/

This model gets the two different ways, first the standard way and
then the Sicherman dice:
  
  x1 = [1, 2, 3, 4, 5, 6]
  x2 = [1, 2, 3, 4, 5, 6]
  ----------
  x1 = [1, 2, 2, 3, 3, 4]
  x2 = [1, 3, 4, 5, 6, 8]


Extra: If we also allow 0 (zero) as a valid value then the 
following two solutions are also valid:
  
  x1 = [0, 1, 1, 2, 2, 3]
  x2 = [2, 4, 5, 6, 7, 9]
  ----------
  x1 = [0, 1, 2, 3, 4, 5]
  x2 = [2, 3, 4, 5, 6, 7]
  
These two extra cases are mentioned here:
http://mathworld.wolfram.com/SichermanDice.html


Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my CPMpy page: http://www.hakank.org/cpmpy/
"""
from cpmpy import *
import numpy as np
from instances.cpmpy_hakank import *


def sicherman_dice(min_val=0):

  n = 6
  m = 10

  # standard distribution
  standard_dist = [1,2,3,4,5,6,5,4,3,2,1]

  # the two dice
  x1 = intvar(min_val, m,shape=n,name="x1")
  x2 = intvar(min_val, m,shape=n,name="x2")

  model = Model (
      [ standard_dist[k] == sum([x1[i] + x2[j] == k+2 for i in range(n) for j in range(n)])
                                                      for k in range(len(standard_dist))],
      [x1[i] <= x1[i+1] for i in range(n-1)],
      [x2[i] <= x2[i+1] for i in range(n-1)],
      [x1[i] <= x2[i] for i in range(n-1)],                        
      )

  return model

def get_model(seed=0):
  return sicherman_dice(1)


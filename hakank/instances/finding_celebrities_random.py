"""
Finding celebrities problem in cpmpy.

From Uwe Hoffmann
'Finding celebrities at a party'
http://www.codemanic.com/papers/celebs/celebs.pdf
'''
Problem: Given a list of people at a party and for each person the list of
people they know at the party, we want to find the celebrities at the party. 
A celebrity is a person that everybody at the party knows but that 
only knows other celebrities. At least one celebrity is present at the party.
'''
(This paper also has an implementation in Scala.)

Note: The original of this problem is 
  Richard Bird and Sharon Curtis: 
  'Functional pearls: Finding celebrities: A lesson in functional programming'
  J. Funct. Program., 16(1):13 20, 2006.

The problem from Hoffmann's paper is to find of who are the 
celebrity/celebrities in this party graph:
  Adam  knows {Dan,Alice,Peter,Eva},
  Dan   knows {Adam,Alice,Peter},
  Eva   knows {Alice,Peter},
  Alice knows {Peter},
  Peter knows {Alice}

Solution: the celebrities are Peter and Alice.

I blogged about this problem in 'Finding celebrities at a party'
http://www.hakank.org/constraint_programming_blog/2010/01/finding_celebrities_at_a_party.html

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my CPMpy page: http://www.hakank.org/cpmpy/

"""
import random
from cpmpy import *
import numpy as np
from instances.cpmpy_hakank import *

def random_01_graph(n):
    return [ [random.randint(0,1) for _ in range(n)] for _ in range(n)] 


def finding_celebrities(problem):

  graph = problem
  n = len(graph)
  
  model = Model()

  # variables
  
  celebrities = boolvar(shape=n,name="celebrities") # 1 if a celebrity
  num_celebrities = intvar(0,n,name="num_celebrities")

  # constraints
  model += (num_celebrities == sum(celebrities))
   
  # All persons know the celebrities,
  # and the celebrities only know celebrities.
  for i in range(n):
    # All persons know the celebrities 
    # model += ((celebrities[i] == 1) == (sum([graph[j][i] for j in range(n)]) == n))
    
    # The celebrities only know each other
    # model += ((celebrities[i] == 1) == (sum([graph[i][j] for j in range(n)]) == num_celebrities))

    model += celebrities[i] == ((sum([graph[j][i] for j in range(n)]) == n) & (sum([graph[i][j] for j in range(n)]) == num_celebrities))

  return model


def get_model(seed=0):
  random.seed(seed)
  problem = random_01_graph(10)
  return finding_celebrities(problem)



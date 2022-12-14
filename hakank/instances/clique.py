"""
Global constraint clique in cpmpy.

From Globals constraint catalogue:
http://www.emn.fr/x-info/sdemasse/gccat/Cclique.html
'''
Consider a digraph G described by the NODES collection: to the ith 
item of the NODES collection corresponds the ith vertex of G; To
each value j of the ith succ variable corresponds an arc from the 
ith vertex to the jth vertex. Select a subset S of the vertices of G 
that forms a clique of size SIZE_CLIQUE (i.e., there is an arc
between each pair of distinct vertices of S).

Example
[The graph is 
  1 -> 2,4
  2 -> 1,3,5
  3 -> 2,5
  4 -> 1,5
  5 -> 2,3,4
]

    (3,<
    index-1	succ-{},
    index-2	succ-{3,5},
    index-3	succ-{2,5},
    index-4	succ-{},
    index-5	succ-{2,3}
    >
    )

The clique constraint holds since the NODES collection depicts a 
clique involving 3 vertices (namely vertices 2, 3 and 5) and since 
its first argument SIZE_CLIQUE is set to the number of vertices of 
this clique.
'''


Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys, random
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *



def check_clique(graph,type="all",card1=None):

    n = len(graph)

    # variables
    x = boolvar(shape=n,name="x")
    card = intvar(0,n,name="card")

    if type == "max":
      model = Model(maximize=card)
    else:
      model = Model()

    # constraints
    if card1 != None:
      model += (card == card1)
      
    model += (clique(graph,x, card))

    return model

#
# make a symmetric random graph (0/1) of size 
#
def random_graph(n):
  g = {}
  for i in range(n):
    for j in range(n):
      if i == j:
        g[(i,j)] = 1
      else:  
        g[(i,j)] = random.randint(0,1)
        g[(j,i)] = g[i,j]
  # Translate 
  return [ [g[(i,j)] for j in range(n) ] for i in range(n)]
    
  

# Two cliques: (0,1,3) and (2,4)
graph1 = [[1, 1, 0, 1, 0], # 0,1,3
          [1, 1, 0, 1, 0], # 0,1,3
          [0, 0, 1, 0, 1], # 2,4
          [1, 1, 0, 1, 0], # 0,1,3
          [0, 0, 1, 0, 1]] # 2,4

#
# A larger graph
# The cliques are 
#   0,1,2
#   3,4,5
#   5,6,7,8,9  
# (and their sub cliques)
#
graph2 =[[1, 1, 1, 0, 0, 0, 0, 1, 0, 0],
         [1, 1, 1, 0, 0, 0, 0, 0, 1, 0],
         [1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
         [0, 1, 0, 1, 1, 1, 0, 0, 0, 0],
         [0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
         [0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
         [0, 0, 1, 0, 0, 1, 1, 1, 1, 1],
         [1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
         [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
         [0, 1, 0, 0, 0, 1, 1, 1, 1, 1]]
       

# The graph from the Global Constraint catalogue (the example above)
# 
# 1 -> 1,3
# 2 -> 0,2,4
# 3 -> 1,4
# 4 -> 0,4
# 5 -> 1,2,3
#   
# The found (maximal) clique (N=3) is {1,2,4}.
#
graph3 = [[1,1,0,1,0],
          [1,1,1,0,1],
          [0,1,1,0,1],
          [1,0,0,1,1],
          [0,1,1,1,1]]


#
# A random graph of size 100 (generated by another program).
# There are 3515 clique of size >= 3 (including sub cliques], 
# and four of size 6.
#
graph4 = [[0,0,1,0,1,0,1,0,0,1,0,1,0,1,1,1,1,0,1,0,0,1,0,1,1,0,1,0,0,0,1,0,1,1,0,1,1,1,0,0,0,1,0,1,1,0,1,0,1,1,0,1,1,0,0,1,0,1,1,1,1,1,1,0,1,0,0,1,1,0,1,1,1,1,1,0,0,1,0,0,0,1,1,1,1,1,1,0,0,1,1,1,0,0,0,1,1,1,1,1],
[1,0,0,1,1,0,0,1,0,0,0,0,0,0,1,1,0,1,0,0,0,0,1,1,1,0,1,1,1,0,0,0,1,1,0,1,0,0,1,1,0,0,0,0,0,1,0,0,1,1,0,1,0,0,0,0,0,1,0,0,0,0,1,1,1,1,1,0,1,0,0,0,0,0,1,1,0,0,1,1,0,1,1,0,1,0,1,0,0,1,0,0,0,0,0,1,0,1,0,1],
[1,0,0,0,0,0,1,0,0,1,1,0,0,1,1,0,0,0,1,0,1,0,0,1,1,0,1,0,1,1,1,1,1,1,1,0,1,1,0,0,0,1,1,0,0,0,1,0,1,1,0,0,0,1,1,0,0,0,0,1,1,1,0,0,1,1,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,1,1,1,0,0,0,0,0,1,1,0,0,0,1,1],
[0,0,0,1,1,1,0,1,1,1,0,0,1,1,0,1,1,0,1,0,1,1,0,0,0,0,0,1,1,0,1,1,1,1,1,1,1,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,1,0,1,0,1,0,0,1,1,1,1,1,1,1,0,1,1,0,0,1,0,1,0,0,1,1,1,1,1,0,1,1,1,0,0,0,1,1,1,0,1,1,1,0,1,0,1,1],
[1,0,0,0,0,1,0,0,1,1,0,0,0,0,1,1,0,0,1,1,0,0,0,1,1,1,0,0,1,1,1,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,1,0,1,1,0,1,0,1,0,0,0,1,0,1,0,1,1,0,1,0,0,1,0,1,0,0,0,0,0,1,0,1,1,1,1,1,0,0,1,0,0,0,0,1,0,0,1,1,1,1,1,1,1,0],
[1,0,1,1,0,0,1,1,1,1,1,0,0,0,1,1,0,0,1,0,1,1,1,0,0,0,0,0,1,1,0,0,0,0,1,1,1,0,0,1,0,1,0,1,0,0,0,0,1,1,0,0,1,1,1,0,1,1,0,1,0,1,0,0,1,0,1,1,1,1,0,0,1,1,0,1,1,0,1,0,0,1,1,0,0,1,1,0,1,0,1,1,1,0,1,1,0,0,1,1],
[1,0,0,1,1,0,1,1,0,1,1,0,0,0,0,0,0,1,1,0,1,0,0,0,0,1,1,0,1,0,0,0,1,0,1,1,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,0,1,1,1,0,1,1,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,1,1,0,1,1,0,0,0,0,1,1,1,0,1,1,0,1,0,0,1,0,0,1,1,0,0],
[1,0,1,0,0,1,0,1,1,1,0,1,1,0,1,0,0,1,1,1,0,1,0,1,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,1,1,0,1,0,0,1,1,0,0,1,1,1,0,1,1,1,0,0,0,1,1,1,0,1,0,1,0,0,0,0,0,1,1,1,0,1,0,1,0,1,1,1,0,0,1,0,1,1,0,1,0,1],
[1,0,0,1,1,1,1,0,0,0,0,1,1,1,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,0,1,1,1,0,1,0,0,0,0,0,1,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,1,0,0,0,1,0,1,1,1,0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,1,1],
[0,1,0,1,0,1,1,1,1,0,0,1,0,1,0,1,1,0,0,1,1,1,0,1,0,0,1,0,0,1,1,1,1,0,0,0,1,1,1,0,1,1,1,1,1,1,0,1,0,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,0,0,1,1,0,1,0,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,1,1,1,1,0,1,1,1,1,0,0],
[1,0,0,0,0,1,0,1,0,1,1,1,0,1,1,1,1,0,1,0,0,0,0,0,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,0,0,0,0,0,0,1,1,1,1,0,0,1,0,0,1,1,0,1,0,0,1,1,0,1,0,0,0,0,0,1,0,0,0,1,0,1,1,0,1,1,1,1,0,0,0,0,1,1,0,0,0,0,0,1,0,1,1,0,0,0],
[0,0,1,1,1,0,1,0,0,0,1,0,0,1,0,1,0,0,1,1,0,0,0,1,0,0,0,1,1,0,1,0,1,0,0,0,1,1,1,1,0,1,0,1,1,0,0,1,0,0,1,1,1,1,0,0,1,1,0,1,0,1,1,0,1,1,0,1,1,1,0,0,0,1,1,0,1,1,0,1,0,1,0,1,1,0,0,1,1,1,1,1,0,1,1,0,1,1,0,0],
[1,1,0,0,0,0,1,0,1,0,1,1,0,1,0,1,1,1,1,1,0,0,0,1,0,1,1,1,0,1,0,0,0,0,1,0,0,1,0,1,0,0,1,0,1,1,1,0,0,0,0,1,0,1,0,0,0,0,1,1,0,1,0,0,0,0,0,0,1,1,0,0,1,1,1,1,0,0,1,0,1,0,0,1,0,0,0,1,1,1,1,1,0,1,1,1,1,0,0,1],
[1,1,1,0,0,0,0,0,0,1,0,1,1,1,0,1,1,0,0,0,0,1,0,0,0,0,1,1,1,1,0,0,1,1,0,0,1,0,1,0,1,1,1,0,0,0,1,0,1,1,1,1,1,0,0,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,1,1,0,0,1,0,1,1,1,0,0,0,1,0,0,0],
[0,0,1,1,1,1,0,1,0,1,0,0,0,0,0,1,0,0,1,1,1,0,0,0,1,0,1,1,0,0,0,0,1,0,0,0,0,0,0,1,1,1,1,1,0,1,0,0,1,0,1,1,1,1,1,0,0,0,1,1,0,1,1,0,0,1,0,0,0,1,0,1,1,1,0,0,0,0,0,1,1,0,1,0,0,1,1,0,0,0,1,1,1,0,0,1,0,1,1,0],
[1,0,0,1,1,0,1,1,1,1,0,1,1,1,1,0,0,0,0,1,1,1,0,0,1,0,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,0,1,1,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0,1,0,1,0,1,0,0,1,1,0,1,1,1,1,0,0,1,0,1,0,1,0,1,1,0,1,1,0,1,0,1,0,1,1,1,0,0,0,1,0,0],
[1,0,0,1,1,1,0,0,1,1,0,1,1,0,0,1,0,0,1,1,1,1,0,0,1,1,0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,0,0,1,0,1,1,1,1,0,0,1,0,0,1,1,1,1,0,0,0,0,0,1,1,1,0,1,0,1,0,0,1,1,0,0,0,1,1,0,0,1,1,1,1,1,1,1,0,1,1,0,0,1,1,1,0,1,1,0],
[0,0,1,0,1,1,1,1,1,0,1,1,1,0,0,1,1,0,0,0,1,0,1,1,0,1,0,0,0,0,1,1,0,1,1,0,1,0,0,1,1,1,0,0,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1,1,1,1,1,0,0,0,0,1,1,0,0,1,0,0,0,1,0,1,0,1,1,0,0,0,1,1,1,0,1,0,0,1,0,1,1,1,0],
[1,1,1,1,0,0,0,1,1,0,0,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,0,1,1,1,0,0,0,0,1,1,1,1,0,1,0,0,1,0,0,0,0,0,1,1,0,1,0,0,0,1,0,0,0,1,1,0,1,0,1,1,0,1,0,0,1,0,0,0,0,1,1,1,0,0,0,1,1,0,0,1,0,0,0,1,1,1,1,1,0,0,0,1,0,1],
[1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,0,0,1,0,1,1,1,1,0,1,0,1,0,0,0,0,1,1,0,1,0,1,1,1,0,1,0,0,1,1,0,0,0,1,0,1,1,1,0,0,1,1,1,1,1,1,0,1,0,1,0,1,0,1,1,0,1,0,1,1,1],
[1,1,0,1,0,0,1,1,1,0,0,1,1,0,1,0,0,0,1,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,1,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1,0,0,1,0,1,1,0,1,1,1,1,1,0,0,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,0,1,0,1,1,1,1,1,1,0,1,1],
[1,1,1,1,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,1,1,0,1,0,1,0,0,0,1,1,1,1,1,0,0,1,1,1,0,0,0,1,1,1,1,1,0,0,0,1,0,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,1,1,1,1,0,0,1,1,1,0,0,1,0,0,0,1,0,0],
[1,0,0,0,0,1,0,0,0,1,0,0,1,1,1,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,1,1,0,0,1,1,0,1,1,1,0,1,0,0,0,0,1,1,1,1,0,1,1,0,1,1,1,0,1,1,1,1,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,0,0,1,1,1,1,0,0,0,1],
[1,0,1,1,1,0,1,0,0,0,1,1,0,0,1,1,1,1,1,0,0,0,1,0,1,0,0,1,1,0,1,0,1,1,0,0,1,1,1,0,1,0,1,0,1,0,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,1,1,1,0,0,0,0,1,1,0,1,1,1,0,0,1,1,1,0,0,0,0,1,0,0,1,1,1,0,1,1,0,1,0,0,1,1,1,0],
[1,0,1,0,0,1,0,0,1,0,1,1,0,0,1,1,0,0,1,0,1,1,0,0,1,0,1,0,1,1,1,1,1,0,1,1,0,0,0,1,1,0,0,0,1,0,1,0,1,1,1,1,0,1,0,1,1,0,1,0,0,1,0,0,0,0,0,0,1,0,1,1,1,0,1,0,0,0,0,0,1,1,1,1,0,1,0,0,0,1,1,0,0,1,0,0,1,0,1,1],
[0,0,1,1,1,0,1,1,1,0,1,1,0,0,0,1,0,1,1,1,0,0,0,0,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,1,1,0,1,1,0,0,1,1,0,0,0,1,1,1,0,0,1,1,0,1,1,0,1,1,0,1,1,0,1,0,0,0,0,1,0,1,1,1,0,0,1,0,1,1,1,1,0,0,1,1,0],
[1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,1,1,1,1,1,0,1,0,1,1,0,0,0,0,1,0,1,1,0,1,0,1,0,0,0,1,0,0,1,1,1,1,0,0,1,0,1,1,1,1,1,0,0,0,0,0,0,1,0,0,1,1,0,0,0,1,0,1,1,0,0,0,1,1,0,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,0,0,0,1],
[1,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0,1,1,0,0,1,0,0,1,1,1,0,1,1,0,1,1,1,1,0,0,1,0,1,0,0,1,0,1,1,1,0,0,0,1,1,0,1,1,0,1,0,1,0,0,0,0,0,1,1,0,1,0,0,1,1,1,0,1,0,0,0,0,1,1,1,1,1,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1],
[1,1,1,1,0,1,0,0,0,1,0,1,0,1,1,0,0,1,1,0,0,0,1,1,1,0,1,1,0,1,1,1,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1,1,0,1,0,1,0,0,1,1,1,1,0,1,1,0,0,0,0,0,0,1,0,1],
[1,0,0,1,1,0,0,1,1,1,0,0,0,1,1,1,0,0,1,1,0,0,0,0,0,1,0,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,0,1,0,0,1,0,1,1,0,1,1,1,0,1,1,1,1,0,0,1,1,1,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0,1],
[0,0,1,1,1,0,0,1,1,0,1,0,0,0,1,0,0,1,0,1,0,1,1,0,1,0,0,1,1,1,0,0,0,1,0,0,1,1,1,0,0,1,1,0,0,1,1,1,1,0,0,0,0,0,0,1,0,0,0,1,0,1,1,1,0,1,0,1,1,1,0,1,0,0,0,1,1,0,1,0,1,1,1,0,0,1,1,1,0,1,1,0,1,1,1,1,1,1,0,0],
[0,0,1,1,0,0,0,1,1,1,0,1,0,0,1,1,1,0,0,0,0,1,1,0,1,1,1,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,1,1,0,1,0,0,1,0,0,1,0,1,1,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,1,0,1,0,0,1,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,1,0,1,0,1,0],
[0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,1,0,0,0,1,1,0,0,1,0,1,1,0,0,0,0,0,0,1,0,1,1,1,0,1,1,0,1,0,1,1,0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,1,0,0,0,1,1,1,0,0,0,1,1,0,1,0,0,1,1,1,1],
[0,1,1,0,0,1,0,1,0,0,0,0,0,1,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,1,0,0,1,1,1,1,1,0,1,1,0,0,1,0,1,1,1,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,1,0,0,0,1,0,1,0,0,1,0,0,0,1,0,1,1,0,0,1,1,0,1,1,0,1,1,1,1],
[0,1,0,1,0,1,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,0,1,1,0,0,1,1,1,1,1,1,0,0,0,1,0,1,0,1,1,1,0,0,1,0,0,0,1,1,1,0,1,1,1,0,0,0,1,1,0,0,1,1,1,0,1,0,1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,1,1,0,0,1,1,1,0,0,0,0,0],
[1,0,0,0,1,0,0,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,1,1,0,1,1,1,0,1,1,0,0,0,1,1,0,0,1,0,0,0,1,1,1,0,1,1,1,1,1,1,0,0,1,0,0,0,1,1,0,0,1,1,1,1,0,1,0,1,1,1,1,0,0,0,0,1,1,0,1,0,0,0,0,1,1,1,1,0,0,1,0,1,1,0,0],
[0,1,1,1,0,1,1,0,0,0,0,0,1,1,1,1,0,1,0,0,0,1,1,0,1,1,0,1,1,1,0,0,0,1,0,1,0,1,0,0,1,0,0,1,1,1,0,0,1,0,0,0,0,1,0,1,0,1,0,1,0,1,1,0,0,0,0,1,0,0,1,0,1,0,1,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1],
[0,1,1,0,0,0,0,0,1,1,1,1,1,1,1,0,1,0,0,0,0,1,1,0,0,1,1,1,0,0,0,0,1,0,1,0,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,1,0,0,0,0,1,1,1,1,0,0,1,1,1,1,0,1,0,0,0,0,0,1,1,0,0,1,1,0,1,1,1],
[1,0,0,1,0,1,0,0,0,0,1,1,0,1,1,0,0,1,1,1,0,1,1,1,0,0,0,1,1,0,1,1,1,1,0,0,1,1,1,0,1,0,1,0,0,0,1,1,1,0,0,1,1,0,0,0,0,1,1,0,1,0,1,1,0,0,1,1,0,1,1,0,1,1,0,1,1,1,0,0,1,0,0,1,1,1,0,0,1,0,0,1,0,1,0,0,0,1,0,1],
[0,0,1,0,0,0,1,1,0,1,1,0,1,1,1,0,1,1,1,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,1,1,1,1,0,1,1,0,0,0,0,1,0,0,1,0,0,0,0,1,1,0,1,0,1,0,0,0,1,0,1,0,0,1,0,0,1,0,0,0,1,1,0,0,0,0,0,1,1,1,0,0,1,1,1,1,0,1,0,0,1,1,0,0,0],
[1,0,0,1,0,0,0,1,1,0,1,1,0,0,1,1,1,1,1,1,0,1,1,1,0,1,1,0,1,1,0,0,0,0,0,1,0,0,1,0,0,0,1,1,1,0,1,0,1,1,1,0,1,1,0,0,0,0,0,1,1,1,1,0,0,0,1,0,0,0,1,0,0,1,1,1,1,1,0,1,1,1,1,0,0,0,0,1,0,0,1,1,0,0,1,0,1,0,1,0],
[1,0,0,0,0,0,1,1,0,1,1,0,1,1,0,1,0,1,1,1,0,0,1,0,1,1,0,1,1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,1,1,1,0,1,1,1,1,0,0,0,1,1,1,1,1,0,1,0,0,1,1,1,1,0,1,1,0,1,1],
[0,0,1,1,1,0,1,0,1,1,1,1,0,1,0,0,1,1,0,0,1,1,0,1,0,1,1,1,0,0,0,0,1,1,0,1,1,0,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,1,1,0,1,1,1,0,0,0,1,0,0,0,0,1,0,1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,1,0,0,1,1,0,0,1,1,0,1,0,1,0,1],
[1,1,0,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,1,1,1,1,0,1,0,1,1,1,0,0,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,0,0,0,1,0,0,1,0,0,0,1,1,0,1,1,0,0,0,1,0,1,1,1,0,0,0,0,1,0,1,1,1,1,0,0,0,1,0,0,0,1],
[0,0,1,0,1,1,1,1,1,0,1,0,0,0,0,1,1,1,1,0,0,1,0,0,1,1,1,0,1,1,0,1,1,1,0,0,0,1,0,0,1,1,1,1,1,1,1,1,1,0,0,1,0,0,1,1,0,0,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,0,1,0,0,0,1,1,1,0,0,1,1,1,0,1,0,1,0,0,0,1,1,0],
[0,0,1,1,0,1,0,1,1,1,0,1,0,0,1,0,0,0,0,1,1,0,0,1,1,0,1,1,0,0,1,0,0,0,1,0,0,1,1,0,0,0,0,0,1,1,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,1,1,0,1,0,0,1,0,1,0,0,0,1,0,1,1,0,0,1,0,0],
[0,1,0,0,1,1,0,1,0,0,1,1,1,1,1,1,1,0,1,1,1,1,0,1,0,1,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,1,1,1,0,0,0,1,1,1,1,0,0,1,0,1,1,1,0,1,0,0,1,1,1,0,0,1,0,1,0,0,1,0,0,1,0,1,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0],
[1,0,0,1,0,0,1,0,0,0,0,0,1,0,0,1,1,0,0,0,1,0,1,1,0,0,1,1,1,1,1,1,0,1,0,0,0,0,0,1,1,1,1,1,0,0,1,1,0,0,1,1,0,0,1,0,0,1,0,1,0,1,1,1,0,1,1,0,0,0,0,0,0,1,1,0,0,1,0,0,1,1,1,1,1,0,1,0,1,0,1,1,1,1,0,1,0,1,1,1],
[0,1,1,1,0,0,0,1,1,1,1,1,0,1,0,0,1,0,1,1,1,0,1,0,1,1,0,1,0,0,1,1,0,0,1,0,1,0,0,0,0,0,0,0,1,1,0,0,1,0,0,1,0,0,1,0,0,1,1,1,1,1,0,1,0,0,1,0,1,1,1,0,0,1,1,1,0,0,0,1,1,1,1,1,0,1,1,1,0,1,1,1,0,0,1,1,0,1,1,1],
[1,0,1,0,0,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,0,1,0,1,1,0,1,0,1,1,0,1,0,0,0,0,1,0,1,1,1,1,1,0,1,0,1,0,0,0,1,1,0,1,1,0,1,0,0,0,0,0,1,0,0,1,1,1,0,1,1,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,1,0,0,0,0,1,0,0,1,0,0,1,0],
[1,1,1,1,1,1,1,0,0,0,1,0,0,1,1,0,1,1,0,1,1,0,1,0,0,1,1,0,1,1,1,0,1,0,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,0,1,1,0,1,0,0,1,1,1,1,1,1,0,0,1,0,0,1,1,1,1,1,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1],
[1,1,1,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,1,0,1,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,1,0,1,1,0,1,0,0,0,1,0,1,0,0,1,0,1,1,0,1,0,0,1,0,1,0,0,1,0,1,1,0,1],
[1,0,1,0,0,1,0,0,0,0,1,0,1,1,1,1,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,1,0,1,0,0,0,1,1,0,1,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,1,0,0,1,0,0,1,0,1,0,0,1,1,0,0,1,1,0,0,1,0,1,1,1,0,0,0,1,0],
[1,0,0,1,0,0,1,0,1,1,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1,0,1,0,1,1,0,1,0,0,1,1,0,0,1,0,1,1,0,1,1,0,1,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,1,1,1,0,1,0,0,0,1,0,1,0,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,1,0,0],
[1,0,0,0,1,0,1,1,0,0,1,0,0,1,1,1,0,1,0,0,0,1,1,0,0,1,0,1,1,0,0,1,1,0,1,0,1,1,0,0,1,0,1,1,0,1,0,1,0,0,1,0,1,0,1,0,0,1,0,1,1,0,0,1,0,0,0,0,1,0,0,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,1,1,1,1,1,1,1,1,1,0,0,1,1,1],
[1,0,1,0,0,1,1,0,0,0,1,1,1,0,0,1,0,0,0,1,1,1,1,1,0,0,1,0,1,0,0,0,1,1,0,1,1,1,0,0,1,0,0,0,1,0,1,1,1,0,1,1,0,0,0,1,0,1,1,1,1,0,0,0,1,1,1,0,0,0,0,1,0,0,0,0,1,0,1,1,0,1,1,1,0,1,0,1,0,1,1,0,0,0,1,0,0,1,1,1],
[1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,0,1,1,0,0,0,1,0,1,0,0,0,1,0,1,1,1,1,0,1,0,1,1,1,0,0,1,0,0,0,1,1,1,0,0,1,0,0,0,0,1,1,1,0,1,0,1,1,0,1,0,0,0,0,0,1,0,1,1,1,0,1,0],
[1,0,0,0,1,0,0,0,0,1,0,1,1,0,1,0,1,0,0,0,0,1,1,0,0,0,0,1,0,1,0,1,1,1,0,1,0,0,1,0,0,1,0,1,1,1,0,0,0,1,1,1,0,0,1,0,1,0,0,0,0,1,0,0,0,1,1,1,0,0,1,1,0,1,0,1,1,1,0,1,1,1,0,0,1,1,1,0,1,0,0,1,1,1,1,1,0,0,1,1],
[1,0,0,1,0,1,0,0,1,1,0,0,0,1,1,0,1,0,1,0,1,1,1,0,0,1,0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,1,1,1,1,0,0,1,0,0,1,1,0,0,0,1,0,0,0,0,0,0,1,0,0,1,0,1,1,1,1,0,0,0,1,0,1,1,1,0,0,1,1,1,1,1,0,1,0,0,0,0,0,1,0,0,1,0,0,0],
[1,0,1,1,0,0,0,0,0,1,0,0,0,1,1,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,1,1,0,1,0,0,1,0,1,1,1,0,1,0,1,0,1,0,1,1,0,1,0,1,1,0,1,1,0,1,0,0,0,0,1,0,1,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0],
[0,0,0,0,1,0,0,0,1,1,1,0,1,0,0,0,0,1,0,0,0,1,1,1,0,0,1,1,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,1,0,0,1,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,0,1,0,0,0,1,1,1,1,0,1,0,1,0,1,0,0,0,0,1,0,1],
[0,1,1,0,0,1,1,1,1,0,0,0,1,1,1,0,0,1,1,0,1,1,1,0,0,1,0,0,0,1,1,1,0,1,0,1,0,0,1,0,1,1,0,0,1,0,0,0,1,0,0,1,1,1,1,0,0,1,0,0,0,1,1,1,0,0,1,0,0,1,1,0,1,1,1,0,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0,0,1,0,1,1,0,0,0,1],
[1,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,1,0,0,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,0,1,1,1,0,0,0,1,0,1,1,1,0,0,0,0,1,0,0,1,0,1,1,1,0,1,0,1,0,1,1,0,0,1,0,0,1,1,1,1,0,0,0,0,1,1,0,1,0,1,1,0,1,1,0,0,1,1,1,0],
[1,1,0,1,1,1,1,0,0,0,1,0,0,0,0,0,1,1,1,1,0,1,1,0,1,0,1,1,1,0,1,0,0,0,0,0,1,1,0,1,0,0,1,0,0,0,1,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1,0,1,0,1,1,1,0,0,0,0,0,1,0,0,1,1,0,0,0,1,1,1,0,1,1,1,0,1,0,1,1,0,0,1,0,1,0],
[1,1,0,1,1,0,1,0,0,0,1,0,0,0,0,1,1,1,0,1,1,0,0,1,1,1,0,1,1,1,1,1,0,1,1,0,0,0,1,1,1,1,1,1,1,0,1,1,1,1,0,1,0,1,1,1,1,0,0,1,1,0,1,1,0,1,0,1,0,1,1,0,0,1,1,0,1,0,0,0,1,1,0,1,1,0,1,1,0,1,1,0,0,1,1,1,0,0,0,0],
[1,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,1,0,0,0,1,0,1,1,1,0,0,0,0,0,0,1,0,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,0,1,1,1,1,1,1,1,0,1,1,0,0,1,1,1,0,0,1,0],
[1,0,0,1,1,0,0,1,1,0,0,0,0,1,0,1,0,1,1,0,0,0,1,0,0,0,1,1,1,0,1,1,1,0,0,1,1,0,0,0,0,1,0,1,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,0,0,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,1,0,0,1,0,0,0,0,0],
[0,0,0,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,1,1,0,1,0,0,1,1,0,0,1,0,0,1,0,1,1,0,0,1,1,1,0,0,1,0,1,0,1,0,0,0,0,0,1,1,0,0,0,1,0,0,1,0,1,1,1,0,0,0,1,0,1,0,1,1,0,0,1,1,1,1,1,0,0,0,1,1,1,0,1,1,1,1,0,1,1,0,1,1,1,0],
[1,0,1,0,0,1,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,1,0,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,1,1,1,1,0,1,1,1,0,1,0,1,0,1,0,1,1,0,0,1,1,1,1,0,0,1,0,1,0,0,1,1,0,1,1,0,1,0,0,0,1,0,1,0,0,1,0,0,1,0,0,0,1,1,1,1],
[1,1,1,0,1,0,1,0,1,0,0,0,1,0,1,1,0,1,1,1,0,1,1,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,0,1,1,0,1,0,1,1,0,1,1,0,0,1,0,1,1,1,1,1,0,0,1,1,0,0,0,0,0,1,1,0,1,1,1,0,1,0,0,0,0,1],
[0,1,1,1,0,0,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,0,0,0,0,1,1,0,0,0,1,1,1,0,0,0,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,1,0,1,1,0,1,0,1,0,1,1,0,1,1,1,1,1,0,0,1,0,0,0,0,1,1,0,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,0,0,0,0,0,1],
[1,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,1,1,0,0,1,0,0,1,0,0,0,0,0,1,0,1,1,0,0,0,1,0,1,1,0,1,0,1,1,1,1,1,1,0,0,1,0,1,0,1,1,1,0,1,0,0,0,0,1,0,1,1,1,0,0,1,1,1,0,1,1,1,0,0,0,1,0,0,0,1,1,0,1,0],
[0,0,0,1,1,0,1,1,1,0,0,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,1,0,1,0,1,0,1,0,0,1,0,1,1,0,0,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,0,0,1,1,0,0,1,1,1,0,1,0,1,1,0,1,0,0,0,1,1,1,1,1,1,0,1,1,0,1,1,0,0,1,0,1,1,1],
[0,1,1,1,0,1,1,0,0,1,1,0,0,1,0,0,0,1,1,1,0,1,1,0,0,0,0,0,0,1,1,1,0,1,1,1,0,1,1,1,1,0,1,0,0,0,0,0,1,1,1,0,1,1,0,1,0,0,1,0,1,0,1,1,0,1,0,0,0,0,1,1,0,1,1,1,0,0,0,0,1,0,0,0,0,1,1,0,0,1,1,1,0,0,1,0,1,1,0,0],
[0,0,1,0,1,0,0,1,0,0,0,1,1,0,1,1,1,0,0,0,0,0,1,1,0,0,0,1,1,1,1,0,1,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,0,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,0,0,0,1,0,0,1,1,1,0,0,1,1,0,1,0,0,0,1,0,0,0,1,1,0,1,1,0,1],
[0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,1,1,0,0,0,1,1,1,1,1,0,0,1,0,1,0,0,1,1,0,0,1,0,0,0,1,0,0,1,1,0,0,1,1,0,1,0,1,0,1,1,1,1,0,0,0,1,1,0,1,0,0,1,1,1,1,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,1,1,0,1,1,0,0,1,0,0],
[1,1,1,0,0,0,0,0,0,0,1,0,1,1,0,1,1,0,1,0,0,0,1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,1,1,1,0,1,1,1,0,1,1,0,1,1,1,0,0,1,0,1,0,0,0,0,1,1,0,1,1,1,0,1,1,0,1,0,1,1,0,1,1,0,1,0,1,0,0,1,0,0,1,1,1,1,0,1,0,1,0,0,1,1,1,0],
[1,1,1,1,0,1,0,0,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,0,0,1,1,1,1,1,1,1,1,0,1,0,0,0,1,1,0,1,1,1,1,1,0,0,0,0,0,1,0,0,0,1,1,1,1,1,1,0,1,1,0,0,1,1,1,1,0,0,0,1,0,0,0,0,1,0,1,1,0,0,0,1,1,1,0,1,0,1,0,1,1,0,1,0,1,0],
[0,0,0,1,1,1,1,0,1,0,1,0,0,0,0,0,1,1,1,0,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0,1,1,0,1,0,1,0,1,0,0,1,1,1,0,1,0,0,0,0,0,1,1,1,0,0,0,0,1,1,0,1,1,0,1,0,1,0,0,0,1,1,0,1,1,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
[0,0,0,1,1,0,1,1,1,0,0,0,0,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,0,1,0,0,0,1,0,0,0,0,1,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0,1,1,1,0,0,1,1,0,1,0,1,0,1,1,1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0],
[0,1,1,0,0,1,1,1,0,1,0,0,1,1,1,0,1,1,1,0,1,0,1,1,1,1,0,0,1,1,0,1,0,0,0,1,1,0,1,0,1,1,0,1,1,1,1,1,0,1,1,1,1,0,0,1,1,0,0,0,1,1,1,0,1,1,0,1,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,0,1,0,1,1,0,1,1,0,0,0,1],
[0,0,0,0,1,0,0,1,1,1,0,1,0,0,0,0,1,0,1,1,0,0,0,0,0,1,1,1,1,1,0,1,0,0,1,0,1,0,1,1,0,0,1,1,1,1,0,1,1,1,0,1,1,0,0,0,1,1,1,0,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,1,1,0,1,0,1,0,1,0,0,1,0,0,0,1,0,1,1,1,0,1,1,1,1,0],
[1,0,1,1,1,0,1,1,0,1,1,0,1,0,0,0,1,0,0,0,1,1,1,0,0,0,0,0,0,1,0,1,1,0,1,0,0,0,1,0,0,1,0,0,1,1,0,0,1,1,0,0,0,0,0,1,1,0,1,1,0,0,0,1,1,1,1,1,1,1,0,0,1,1,1,0,0,1,0,1,0,1,0,1,1,0,0,0,1,1,0,0,0,0,1,0,1,0,0,0],
[0,1,0,0,1,0,0,1,1,1,1,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,0,0,1,1,0,1,0,1,1,1,0,0,1,1,0,1,0,1,1,1,0,1,1,0,0,0,0,1,0,0,0,1,1,1,1,1,1,1,0,1,0,1,0,0,1,1,1,1,1,0,0,1,0,0,0,0,0,0,1,0,0,0,1,1,0],
[0,0,0,1,0,0,1,0,0,0,1,1,1,0,0,1,1,0,0,1,0,1,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,1,0,0,1,1,0,1,0,1,0,0,1,0,0,0,0,0,0,1,0,1,1,0,0,1,1,0,1,1,0,1,0,0,1,1,0,1,0,1,1,1,1,0,1,1,1,0,1,1,0,0,1,1,0,1,1,0,1,1,0,1,0],
[1,1,1,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,1,1,1,0,0,0,1,1,1,1,0,1,1,1,1,0,1,1,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,1,0,1,1,1,1,1,0,0,1,0,1,1,0,1,0,0,0,1],
[1,0,1,1,0,0,1,0,1,0,0,0,1,0,1,0,1,0,1,1,1,1,1,1,0,1,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,1,0,1,0,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,0,1,0,1,0,1,0,1,1,0,1,0,0,1,0,0,0,1,1,1,0,1,1,1,1,1,0,0,0,0,1,0,1,0,0,0,1,1,1],
[1,1,0,0,0,1,0,0,1,1,1,0,0,0,1,0,0,0,1,1,0,0,1,0,0,1,0,1,1,1,1,0,1,0,1,0,1,0,0,0,0,1,0,0,1,0,0,0,0,1,0,1,1,0,0,1,0,1,1,1,1,0,0,1,1,1,0,1,1,0,1,0,0,1,0,0,0,1,1,1,0,0,1,0,1,1,1,1,1,0,1,0,0,0,1,0,0,1,1,0],
[1,0,1,1,1,0,1,0,0,0,0,1,1,0,0,0,1,0,1,0,0,1,0,1,0,1,0,1,1,0,0,0,0,0,0,1,0,1,0,1,1,1,0,1,0,1,0,0,1,0,1,1,0,0,1,1,0,1,1,0,0,1,1,0,1,1,0,0,0,0,1,1,1,1,0,1,0,0,0,1,1,0,0,0,1,1,1,1,0,1,1,0,1,0,1,0,0,1,1,1],
[1,0,0,0,1,1,0,1,0,0,1,1,1,0,0,1,0,0,1,0,1,1,1,0,0,1,1,1,1,1,1,0,1,1,0,0,1,1,1,1,1,1,0,0,0,1,0,0,1,1,0,1,0,1,0,1,1,0,0,0,1,1,0,0,0,0,0,1,0,0,1,1,0,0,1,0,0,0,1,1,0,0,1,1,0,1,0,0,0,1,0,1,0,1,0,0,0,0,1,0],
[1,0,1,0,1,1,1,0,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,1,1,0,1,0,1,1,0,1,1,1,0,1,1,0,0,1,0,1,0,0,0,0,1,0,0,0,0,1,1,0,0,1,0,0,1,1,1,0,0,0,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0],
[0,1,0,0,1,0,0,1,1,0,1,0,1,1,1,1,1,0,1,0,0,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,0,1,0,0,1,1,0,0,1,1,1,1,0,0,1,0,0,1,1,1,1,1,0,0,1,0,1,1,0,1,0,1,1,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,1,0,0,0,0,1,0,1,0,1],
[0,1,0,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,1,0,1,0,1,1,1,1,0,0,1,1,0,0,1,1,0,1,1,0,0,0,1,0,0,1,0,0,0,1,1,0,0,1,0,0,1,0,0,0,1,1,1,1,1,1,1,0,1,1,1,1,0,1,0,0,1,1,0,0,1,0,0,1,1,0,0,1,1,1,0,0,1,0,0,1,0,1,1,1],
[0,0,0,1,0,0,1,0,0,1,1,0,0,0,1,0,0,0,1,1,1,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,0,1,1,1,0,1,1,0,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,0,1,0,1,0,0,1,1,0,1,1,1,0,1,0,0,0,1,0,1,1,1,1,0,1,1,0,0,1,1,0,0,0,1,0,1,0,0,0,1],
[1,0,1,1,0,1,0,1,0,0,0,1,0,0,1,0,1,0,1,0,0,0,0,1,1,0,1,0,0,0,0,1,0,0,0,1,0,1,0,1,0,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,1,0,1,1,0,1,0,0,1,0,0,0,1,1,0,1,1,1,0,0,0,0,0,0,0,1,1,0,0,1,0,0,1,1,1,1,1,0,0],
[0,0,0,1,0,1,0,1,0,1,1,0,0,1,0,0,1,1,1,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,1,1,0,1,0,0,0,0,0,1,0,0,0,1,1,0,1,0,1,1,1,0,0,0,1,0,1,0,0,1,1,1,1,0,0,0,0,1,0,0,1,1,1,1],
[0,0,0,1,0,1,1,0,0,0,1,0,1,1,0,0,1,0,1,0,1,1,1,0,1,0,0,1,1,0,1,1,0,1,0,0,0,0,0,1,0,0,1,0,0,0,1,1,1,0,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,0,0,1,1,1,1,1,1,1,1,1,0,1,1,0,0,0,0,1,1,0,0,1,0,0,0,0,1,0,0,0,1,0,1,1],
[0,1,1,1,1,1,1,1,1,0,0,0,0,1,0,1,0,0,0,0,1,0,1,0,0,0,0,0,1,1,1,1,1,1,1,0,1,0,1,1,1,0,0,1,0,0,0,0,1,1,0,1,0,1,1,0,1,1,0,1,0,0,0,1,1,0,0,0,0,0,1,1,1,0,1,0,1,1,1,1,1,1,1,0,0,1,1,1,1,0,1,0,0,1,1,1,0,0,0,0],
[1,0,0,1,0,0,1,0,1,1,0,1,0,1,1,0,0,1,1,0,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,1,1,1,0,1,0,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,0,1,0,0,0,1,1,1,1,1,1,1,1,1,1,0,1,0,0,1,0,1,1,1,1,1,0,1,1,0,0,0,1,0],
[1,0,1,0,0,0,0,0,1,1,0,1,1,0,0,1,0,1,1,0,0,0,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,0,0,0,0,1,0,1,0,1,0,0,0,0,1,1,1,0,1,0,0,1,0,1,1,1,1,1,0,0,0,1,1,1,0,1,1,0,1,0,1,1,1,1,0,0,1,1,1,0,1,0,0,1,0,0,1,1,1,0,0,1,0,0]]

def get_model(seed=0):
  random.seed(seed)
  size = int(round(random.uniform(20, 120)))
  return check_clique(random_graph(size))
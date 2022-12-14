"""
K4P2 Graceful Graph in cpmpy.

http://www.csplib.org/Problems/prob053/
'''
Proposed by Karen Petrie
A labelling f of the nodes of a graph with q edges is graceful if f assigns each node a unique label
from 0,1,...,q and when each edge xy is labelled with |f(x)-f(y)|, the edge labels are all different.
Gallian surveys graceful graphs, i.e. graphs with a graceful labelling, and lists the graphs whose status
is known.

[ picture ]

All-Interval Series is a special case of a graceful graph where the graph is a line.
'''

This cpmpy model was written by Hakan Kjellerstrand (hakank@gmail.com)
See also my cpmpy page: http://hakank.org/cpmpy/
  
"""
from cpmpy import *
import cpmpy.solvers
import numpy as np
from instances.cpmpy_hakank import *


def k4p2gracefulgraph2():

  graph = [[0, 1],
           [0, 2],
           [0, 3],
           [1, 2],
           [1, 3],
           [2, 3],
           [4, 5],
           [4, 6],
           [4, 7],
           [5, 6],
           [5, 7],
           [6, 7],
           [0, 4],
           [1, 5],
           [2, 6],
           [3, 7]]


  # data
  q = len(graph)
  n = len(np.unique(graph))

  # variables
  nodes = intvar(0,q,shape=n,name="nodes")
  edges = intvar(1,q,shape=q,name="edges")

  # constraints
  model = Model(AllDifferent(edges),
                AllDifferent(nodes),
                [abs(nodes[s] - nodes[t]) for (s,t) in graph] == edges
           )

  return model

def get_model(seed=0):
  return k4p2gracefulgraph2()
  

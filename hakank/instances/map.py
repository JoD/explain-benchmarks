"""
Map coloring problem in cpmpy.

From Pascal Van Hentenryck 'The OPL Optimization Programming Language',
page 7, 42.


This cpmpy model was written by Hakan Kjellerstrand (hakank@gmail.com)
See also my cpmpy page: http://hakank.org/cpmpy/
  
"""
from cpmpy import *
import cpmpy.solvers
import numpy as np
from instances.cpmpy_hakank import *




def map_model():

  model = Model()

  
  # data
  Belgium = 0
  Denmark = 1
  France = 2
  Germany = 3
  Netherlands = 4
  Luxembourg = 5

  n = 6
  max_num_colors = 4

  # declare variables
  color = intvar(1,max_num_colors,shape=n,name="color")

  #
  # constraints
  #
  model += [color[Belgium] == 1,  # Symmetry breaking
            color[France] != color[Belgium],
            color[France] != color[Luxembourg],
            color[France] != color[Germany],
            color[Luxembourg] != color[Germany],
            color[Luxembourg] != color[Belgium],
            color[Belgium] != color[Netherlands],
            color[Belgium] != color[Germany],
            color[Germany] != color[Netherlands],
            color[Germany] != color[Denmark]]

  return model
def get_model():
  return map_model()

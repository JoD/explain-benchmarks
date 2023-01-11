"""
The Familiy Puzzle in cpmpy.

From Drools Puzzle Round 2: The Familiy Puzzle
http://blog.athico.com/2007/08/drools-puzzle-round-2-familiy-puzzle.html
'''

* Three men, Abel, Locker and Snyder are married to Edith, Doris and Luisa, 
  but not necessarily in this order.
* Each couple has one son.
* The sons are called Albert, Henry and Victor.
* Snyder is nor married to Luisa, neither is he Henry's father.
* Edit is not married to Locker and not Albert's mother.
* If Alberts father is either Locker or Snyder, then Luisa is Victor's mother.
* If Luisa is married to Locker, then Doris is not Albert's mother. 

Who is married to whom and what are their sons called?

Taken from the German book 'Denken als Spiel' by Willy Hochkeppel, 1973 
(Thinking as a Game).  
'''

Solutions and discussions
http://ningning.org/blog2/2008/05/25/drools-puzzles-result-round-2-the-familiy-puzzle
http://rbs.gernotstarke.de/samples/page21/page21.html

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *


def the_family_puzzle():

  n = 3
  
  Abel = 0
  Locker = 1
  Snyder = 2
  men = [Abel, Locker, Snyder]

  # variables
  Edith = intvar(0,n-1,name="Edith")
  Doris = intvar(0,n-1,name="Doris")
  Luisa = intvar(0,n-1,name="Luisa")

  women = [Edith,Doris,Luisa]

  Albert = intvar(0,n-1,name="Albert")
  Henry  = intvar(0,n-1,name="Henry")
  Victor = intvar(0,n-1,name="Victor")

  sons = [Albert,Henry,Victor]

  model = Model([alldifferent(women),
                 alldifferent(sons),

                 # Snyder is nor married to Luisa, neither is he Henry's father.
                 Snyder != Luisa,
                 Snyder != Henry,

                 # Edith is not married to Locker and not Albert's mother.
                 Edith != Locker,
                 Edith != Albert,

                 # If Alberts father is either Locker or Snyder, 
                 # then Luisa is Victor's mother.
                 ((Albert == Locker) | (Albert == Snyder)).implies(Luisa == Victor),

                 # If Luisa is married to Locker, 
                 # then Doris is not Albert's mother. 
                 
                 (Luisa == Locker).implies(Doris != Albert),
                 ])

  return model

def get_model(seed=0):
  return the_family_puzzle()

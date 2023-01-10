"""
Generic alphametic solver in cpmpy.

This is a generic alphametic solver.

Usage:
    python alphametic.py
        ->  solves SEND+MORE=MONEY in base 10

    python alphametic.py  'SEND+MOST=MONEY' 11
        -> solver SEND+MOST=MONEY in base 11

    python alphametic.py TEST <base>
        -> solve some test problems in base <base>
            (defined in test_problems())

Assumptions:
- we only solves problems of the form
    NUMBER<1>+NUMBER<2>...+NUMBER<N-1> = NUMBER<N>
    i.e. the last number is the sum
- the only nonletter characters are: +, =, \d (which are splitted upon)



Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys,re
from cpmpy import *
import numpy as np
from cpmpy_hakank import *


def alphametic(problem_str="SEND+MORE=MONEY", base=10):

  model = Model()

  # data
  print("\nproblem:", problem_str)

  # convert to array.
  problem = re.split("[\s+=]", problem_str)

  p_len = len(problem)
  print("base:", base)

  # create the lookup table: list of (digit : ix)
  a = sorted(set("".join(problem)))
  n = len(a)
  lookup = dict(list(zip(a, list(range(n)))))

  # length of each number
  lens = list(map(len, problem))

  #
  # declare variables
  #

  # the digits
  x = intvar(0,base-1,shape=n,name="x")
  # the sums of each number (e.g. the three numbers SEND, MORE, MONEY)
  sums = [intvar(1, base**(lens[i]) - 1) for i in range(p_len)]
  #
  # constraints
  #
  model += (AllDifferent(x))

  ix = 0
  for prob in problem:
    this_len = len(prob)

    # sum all the digits with proper exponents to a number
    model += (
        sums[ix] == sum([(base**i) * x[lookup[prob[this_len - i - 1]]]
                                for i in range(this_len)[::-1]]))
    # leading digits must be > 0
    model += (x[lookup[prob[0]]] > 0)
    ix += 1

  # the last number is the sum of the previous numbers
  model += (sum([sums[i] for i in range(p_len - 1)]) == sums[-1])

  return model

def get_model(seed=0, base=10):
  import random
  random.seed(seed)
  problems = [
      "SEND+MORE=MONEY", "SEND+MOST=MONEY", "VINGT+CINQ+CINQ=TRENTE",
      "EIN+EIN+EIN+EIN=VIER", "DONALD+GERALD=ROBERT",
      "SATURN+URANUS+NEPTUNE+PLUTO+PLANETS", "WRONG+WRONG=RIGHT",
      "GATHER+HOMAGE=MARTIN"
  ]

  p = random.choice(problems)
  return alphametic(p, base)

"""
Ormat game in cpmpy.

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *

#
# Generate all the overlays for a specific size (n).
#
def get_overlays(n=3, debug=0):

    x = boolvar(shape=(n, n),name="x")
    model = Model (
        [ sum(row) == 1 for row in x],
        [ sum(col) == 1 for col in x.transpose()]        
        )

    # all solution solving, with blocking clauses
    ss = CPM_ortools(model)
    # s.ort_solver.parameters.num_search_workers = 8 # not for SearchForAllSolutions!
    # s.ort_solver.parameters.search_branching = ort.PORTFOLIO_SEARCH 
    # s.ort_solver.parameters.cp_model_presolve = False
    ss.ort_solver.parameters.linearization_level = 0
    ss.ort_solver.parameters.cp_model_probing_level = 0

    overlays = []
    def print_sol():
      overlays.append(x.value())

    ss.solveAll(display=print_sol)

    return overlays



# Generate all the problems of size n
def all_problems(n = 3, debug = 0):
    x = boolvar(shape=(n, n),name="x")

    model = Model (
        
        [ sum(row) >= 1 for row in x],
        [ sum(col) >= 1 for col in x.transpose()], 
        )

    return model
    

#
# This solves a problem instance
#
def ormat_game(problem, overlays, n, debug=0):

    f = len(overlays)
    x = boolvar(shape=f, name="x")
    num_overlays = intvar(0,f,name="num_overlays")

    # Count the number of occurrences for each cell for
    # the choosen overlays.
    # Mainly for debugging purposes, but it also makes the
    # modeling easier.
    y = intvar(0,f,shape=(n,n),name="y")
    y_flat = y.flat
    
    model = Model (
        # sanity clauses
        [ sum(row) >= 1 for row in y],
        [ sum(col) >= 1 for col in y.transpose()],         
        num_overlays == sum(x),
        minimize=num_overlays,
        )

    for i in range(n):
        for j in range(n):           
            model += [y[i,j] == sum([(x[o])*(overlays[o][i][j]) for o in range(f)])]

            # model += [y[i,j] >= problem[i][j]]
            
            if problem[i][j] == 1:
                model += [y[i,j] >= 1]

            if problem[i][j] == 0:
                model += [y[i,j] == 0]


    return model

def get_model(seed=0):

    

    problems = {
        "problem1": {
        "n": 3,
        "problem": [
                [1,0,0],
                [0,1,1],
                [0,1,1]
                ]
        },

        # Problem grid 2
        "problem2" : {
        "n": 3,
        "problem" : [
                [1,1,1],
                [1,1,1],
                [1,1,1]
                ]
        },

        "problem3": {
        "n": 3,
        "problem": [
                [1,1,1],
                [1,1,1],
                [0,1,1]
                ]
        },


    # Note: Before solve y matrix has y2.2 in {} which is very bad, and
    #       is the reason (or a symptom) that this problem shows no solution.
    #
    # x before solve: [x0 in {0,1}, x1 in {1}, x2 in {0,1}, x3 in {1}, x4 in {1}, x5 in {0,1}]
    # y before solve:
    # [[y0.0 in {0..2}, y0.1 in {0,1}, y0.2 in {0..3}],
    # [y1.0 in {0..3}, y1.1 in {0..2}, y1.2 in {0,1}],
    # [y2.0 in {0,1}, y2.1 in {0..3}, y2.2 in {}]]
    #
    # Strange: another run has not this empty domain for y2.2...
    #
    # # Problem grid 3
        "problem4": {
        "n":3,
        "problem":  [
        [1,1,1],
        [1,1,1],
        [1,1,0]
        ]

    },

    # This rotation of the above works
    "problem5": {
        "n": 3,
        "problem": [
        [1,1,1],
        [1,1,1],
        [0,1,1]

        ]
        },

    # This is a _bad_ problem since all rows
    # and colutions must have at least one cell=1
    "problem6": {
        "n": 3,
        "problem" : [
        [0,0,0],
        [0,1,1],
        [0,1,1]
        ]
    },


    # # Problem grid 4 (n = 4)
    "problem7": {
    "n" : 4,
    "problem" : [
        [1,1,1,1],
        [1,1,1,1],
        [1,1,1,1],
        [1,1,0,0]
        ]
    },


    # variant
    "problem8": {
    "n" : 4,
    "problem" : [
        [1,1,1,1],
        [1,1,1,1],
        [1,1,1,1],
        [1,1,1,0]
        ]
    },

    # variant
    "problem9" : {
    "n":4,
    "problem" : [
        [1,1,1,1],
        [1,1,1,1],
        [1,1,1,1],
        [1,1,1,1]
        ]
    },


    # # Problem grid 5 (n = 5)
    # # This is under the section "Out of bounds"
    "problem10": {
    "n" : 5,
    "problem" : [
        [1,1,1,1,1],
        [1,1,1,1,1],
        [1,1,1,1,1],
        [1,1,1,1,1],
        [1,1,0,0,0]
        ]
    },

    # # Problem grid 6 (n = 6)
    "problem11" : {
    "n": 6,
    # This is under the section "Out of bounds"%
    "problem" : [
        [1,1,1,1,1,1],
        [1,1,1,1,1,1],
        [1,1,1,1,1,1],
        [1,1,1,1,1,1],
        [1,1,1,1,1,1],
        [1,1,0,0,0,0]
        ]
    },

    }

    import random
    random.seed(seed)
    p = random.choice(list(problems))
    
    problem = problems[p]["problem"]
    n = problems[p]["n"]
    overlays = get_overlays(n, debug=False)
    return ormat_game(problem, overlays, n, debug=False)

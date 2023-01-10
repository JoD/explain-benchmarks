"""
Manufacturing Cell Design Problem (MCDP) in cpmpy.

'''
Cellular manufacturing is an organizational approach based on
group technology (GT). Cellular manufacturing aims to divide the
plant into a certain number of cells. Each cell contains machines
that process similar types or families of products. Manufacturing
cells (MC) provide considerable cost and productivity benefits to
practical manufacturing environments. Other considerable benefits
to be gained by grouping machines into cells can be found in
literature (Selim, Askin, & Vakharia, 1998).

Eclipse solution by Juan Andres Gutierrez Quezada at Alexis Efrain Lopez Estay
'''

Note: This is a port of the first MCDP model (in MiniZinc) that was the
experimental ground for our two papers:

* Ricardo Soto, Hakan Kjellerstrand, Orlando Duran, Fernando Paredes:
  'Cell Formation a in Group Technology using Constraint Programming and Boolean Satisfiability'
  Expert Systems with Applications 39(13):11423-11427
* Ricardo Soto, Hakan Kjellerstrand, Juan Andres Gutierrez,
  Alexis López, Broderick Crawford, Eric Monfroy:
  'Solving Manufacturing Cell Design Problems Using Constraint Programming'
  Conference: International Conference on Industrial, Engineering and Other Applications of Applied Intelligent Systems


cells:2 mmax:8
machines: 16
parts:  30
cells:  2
mmax:  8
total_cost:  11
Machine assignments:
Cell:  1 :  1 2 6 9 11 13 14 16 
Cell:  2 :  3 4 5 7 8 10 12 15 
Part assignments:
Cell:  1 :  2 5 8 9 10 12 17 20 21 23 24 25 26 27 28 29 30 
Cell:  2 :  1 3 4 6 7 11 13 14 15 16 18 19 22 
status: ExitStatus.OPTIMAL (0.25358104600000003 seconds)


cells:2 mmax:11
machines: 16
parts:  30
cells:  2
mmax:  11
total_cost:  11
Machine assignments:
Cell:  1 :  1 2 6 9 11 13 14 16 
Cell:  2 :  3 4 5 7 8 10 12 15 
Part assignments:
Cell:  1 :  2 5 8 9 10 12 17 20 21 22 23 24 25 26 27 28 29 30 
Cell:  2 :  1 3 4 6 7 11 13 14 15 16 18 19 
status: ExitStatus.OPTIMAL (0.49414698100000004 seconds)


cells:2 mmax:12
machines: 16
parts:  30
cells:  2
mmax:  12
total_cost:  11
Machine assignments:
Cell:  1 :  3 4 5 7 8 10 12 15 
Cell:  2 :  1 2 6 9 11 13 14 16 
Part assignments:
Cell:  1 :  1 3 4 6 7 11 13 14 15 16 18 19 
Cell:  2 :  2 5 8 9 10 12 17 20 21 22 23 24 25 26 27 28 29 30 
status: ExitStatus.OPTIMAL (0.42263557100000004 seconds)


cells:3 mmax:8
machines: 16
parts:  30
cells:  3
mmax:  8
total_cost:  11
Machine assignments:
Cell:  1 :  
Cell:  2 :  3 4 5 7 8 10 12 15 
Cell:  3 :  1 2 6 9 11 13 14 16 
Part assignments:
Cell:  1 :  
Cell:  2 :  1 3 4 6 7 11 13 14 15 16 18 19 
Cell:  3 :  2 5 8 9 10 12 17 20 21 22 23 24 25 26 27 28 29 30 
status: ExitStatus.OPTIMAL (2.0134817270000003 seconds)


cells:3 mmax:11
machines: 16
parts:  30
cells:  3
mmax:  11
total_cost:  11
Machine assignments:
Cell:  1 :  3 4 5 7 8 10 12 15 
Cell:  2 :  
Cell:  3 :  1 2 6 9 11 13 14 16 
Part assignments:
Cell:  1 :  1 3 4 6 7 11 12 13 14 15 16 18 19 22 
Cell:  2 :  
Cell:  3 :  2 5 8 9 10 17 20 21 23 24 25 26 27 28 29 30 
status: ExitStatus.OPTIMAL (7.061891548 seconds)


cells:3 mmax:12
machines: 16
parts:  30
cells:  3
mmax:  12
total_cost:  11
Machine assignments:
Cell:  1 :  
Cell:  2 :  3 4 5 7 8 10 12 15 
Cell:  3 :  1 2 6 9 11 13 14 16 
Part assignments:
Cell:  1 :  
Cell:  2 :  1 3 4 6 7 11 12 13 14 15 16 18 19 
Cell:  3 :  2 5 8 9 10 17 20 21 22 23 24 25 26 27 28 29 30 
status: ExitStatus.OPTIMAL (4.8412888060000006 seconds)


  Also see:
  - http://www.hakank.org/picat/mcdp2.pi
  - http://hakank.org/minizinc/MCDP/index_mcdp.html

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *



def MCDP1(machines, parts, cells, mmax, matrix_machine_part):

    model = Model()

    #print("machines:", machines)
    #print("parts: ", parts)
    #print("cells: ", cells)
    #print("mmax: ", mmax)
    # #print('machines: %i parts: %i cells: %i mmax: %i' % (machines, parts, cells, mmax))

    #
    # Variables
    #


    # 1..Machines, 1..Cells
    # matrix_machine_cell = {}
    # for i in range(machines):
    #     for k in range(cells):
    #         matrix_machine_cell[(i,k)] = solver.IntVar(0, 1, 'matrix_machine_cell(%i,%i)' % (i,k))
    matrix_machine_cell = boolvar(shape=(machines,cells),name="matrix_machine_cell")

    matrix_machine_cell_flat = matrix_machine_cell.flat

    # 1..Machines, 1..Cells
    # matrix_part_cell = {}
    # for j in range(parts):
    #     for k in range(cells):
    #         matrix_part_cell[(j,k)] = solver.IntVar(0, 1, 'matrix_part_cell(%i,%i)' % (j,k))

    # matrix_part_cell_flat = [matrix_part_cell[(j,k)]
    #                             for j in range(parts)
    #                             for k in range(cells)]
    matrix_part_cell = boolvar(shape=(parts,cells),name="matrix_part_cell")

    total_cost = intvar(0, machines*parts,name="total_cost")

    #
    # constraints
    #

    # Ensure max mmax machine in each cell
    for k in range(cells):
        model += (sum([matrix_machine_cell[i,k] for i in range(machines)]) <= mmax)


    for i in range(machines):
        model += (sum([matrix_machine_cell[i,k] for k in range(cells)]) == 1)

    for j in range(parts):
        model += (sum([matrix_part_cell[j,k] for k in range(cells)]) == 1)


    # Cost (to minimize)
    model += (total_cost ==
               sum([matrix_machine_part[i][j]*matrix_part_cell[(j,k)]*(1-matrix_machine_cell[(i,k)])
                           for k in range(cells)
                           for i in range(machines)
                           for j in range(parts)]
                          
                          )
               )

    # objective
    model.minimize(total_cost)
    return model


def get_model(seed=0):
    machines = 16
    parts = 30
    cells = 2
    mmax = 12

                        # 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 
    matrix_machine_part =  [[0,0,0,0,1,0,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,1,0,0,1,0,0,1,0], # 1
                            [0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,1,1,0,0,1,1,1,0,0,0], # 2
                            [0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0], # 3
                            [0,0,1,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1], # 4
                            [0,0,1,1,0,0,0,0,0,0,1,1,1,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0], # 5
                            [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,1,1,1,1], # 6
                            [0,0,0,0,0,0,1,0,0,0,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 7
                            [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0], # 8
                            [0,1,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1,1,0,0,1,0,1], # 9
                            [1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 10
                            [0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,1], # 11
                            [1,0,1,1,0,0,1,0,0,0,1,0,1,0,1,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0], # 12
                            [0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,1,1,0,1,0], # 13
                            [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0], # 14
                            [1,0,1,1,0,0,1,0,0,0,0,0,1,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0], # 15
                            [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,1,1,1,1,1,1,1]]  # 16
    import random
    random.seed(seed)
    cells_vals = [2,3]
    mmax_vals = [8,11,12]

    cells = random.choice(cells_vals)
    mmax = random.choice(mmax_vals)

    return MCDP1(machines, parts, cells, mmax, matrix_machine_part)

    
    




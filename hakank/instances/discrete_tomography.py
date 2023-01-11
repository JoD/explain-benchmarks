"""
Discrete tomography in cpmpy.

Problem from http://eclipse.crosscoreop.com/examples/tomo.ecl.txt
'''
This is a little "tomography" problem, taken from an old issue
of Scientific American.

A matrix which contains zeroes and ones gets "x-rayed" vertically and
horizontally, giving the total number of ones in each row and column.
The problem is to reconstruct the contents of the matrix from this
information. Sample run:

?- go.
    0 0 7 1 6 3 4 5 2 7 0 0
 0                         
 0                         
 8      * * * * * * * *    
 2      *             *    
 6      *   * * * *   *    
 4      *   *     *   *    
 5      *   *   * *   *    
 3      *   *         *    
 7      *   * * * * * *    
 0                         
 0                         


Eclipse solution by Joachim Schimpf, IC-Parc
'''

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *


def discrete_tomography(row_sums="", col_sums=""):

    if row_sums == "":
        #print("Using default problem")
        row_sums = [0,0,8,2,6,4,5,3,7,0,0]
        col_sums = [0,0,7,1,6,3,4,5,2,7,0,0]


    r = len(row_sums)
    c = len(col_sums)

    x = intvar(0,1,shape=(r, c), name="x")

    model = Model([
        [sum(row) == row_sums[i] for (row,i) in zip(x, range(r))],
        [sum(col) == col_sums[j] for (col,j) in zip(x.transpose(), range(c))]
        ]
        )

    return model

#
# Read a problem instance from a file
#
def read_problem(file):
    f = open(file, 'r')
    row_sums = f.readline()
    col_sums = f.readline()
    row_sums = [int(r) for r in (row_sums.rstrip()).split(",")]
    col_sums = [int(c) for c in (col_sums.rstrip()).split(",")]
    
    return [row_sums, col_sums]



def get_model(seed=0):
    import os
    base_path = os.path.realpath(__file__).replace('discrete_tomography.py', '')
    all_files = [
        "discrete_tomography1.txt",
        "discrete_tomography2.txt",
        "discrete_tomography3.txt",
        "discrete_tomography4.txt",
    ]
    import random
    random.seed(seed)
    file = random.choice(all_files)
    [row_sums, col_sums] = read_problem(base_path + file)
    return discrete_tomography(row_sums, col_sums)    

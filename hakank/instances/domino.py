"""
Domino problem in cpmpy.

This cpmpy model was written by Hakan Kjellerstrand (hakank@gmail.com)
See also my cpmpy page: http://hakank.org/cpmpy/

"""
from cpmpy import *
import numpy as np
from cpmpy_hakank import *


#
# Exactly one of A[I,J]'s neighbors is the same as A[I,J]
#
def form_domino(a,i,j,r,c):
    bs = []
    for ii in range(i-1,i+2):
        for jj in range(j-1,j+2):
            if ii >= 0 and ii < r and jj >= 0 and jj < c and (ii == i or jj == j) and [i,j] != [ii,jj]:
                bs.append(a[ii,jj] == a[i,j])
    return [sum(bs) == 1]
              

#
# Gecode presentation
#
# For the 7x8 problem (puzzl1, the Dell puzzle)
# Example:
# 
#   Pieces:
#   10 10  9 27 22  2 14 14
#   20 20  9 27 22  2 21  7
#   26 28 28  8 16 16 21  7
#   26 13  5  8 19  4  4  1
#   25 13  5 18 19 15 24  1
#   25 12 12 18 23 15 24  6
#   11 11  3  3 23 17 17  6
#
#   Gecode's representation:
#   998QL1DD
#   JJ8QL1K6
#   PRR7FFK6
#   PC47I330
#   OC4HIEN0
#   OBBHMEN5
#   AA22MGG5
#
def print_board2(a,d,rows,cols,dmap):
  print("\nAnother representation:")
  n = len(dmap)
  ddd = {t:i for (t,i) in zip([v[0] for v in dmap],range(n))}
  s = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
  for i in range(rows):
    for j in range(cols):
        for ix in range(len(d)):
            if d[ix] == a[i,j].value(): 
                # print("%3s (%s)" % (d[ix],dmap[ix]),end=" ")
                v,ii,jj = dmap[ix]
                print("%2d-%2d" % (ii,jj) ,end=" ")                
    print()
    
  # Can only manage dmaps of size <= 62, e.g. not the sicstus instance).
  if n < len(s):
      print("\nAnd yet another representation:")
      for i in range(rows):
          for j in range(cols):
              print(s[ddd[a[i,j].value()]],end="")
          print()
      print()
  print()

def domino(problem,num_sols=1):

    model = Model()

    #
    # data
    #
    rows = len(problem)
    cols = len(problem[0])
    print("rows:",rows, "cols:",cols)
    
    max_val = max([problem[i][j] for i in range(rows) for j in range(cols)])
    
    # To handle larger instances (i.e. max val > 9)
    # we have to tweak a little
    mod_val = 10
    if max_val < 10:
        mod_val = 10
    else:
        mod_val = max_val + 1

    #
    # Convert each domino piece <a,b> to one number "ab"
    #
    # D=[0,1,6,11,..,16,...,55,56,66]
    dmap = [(i*mod_val+j,i,j) for i in range(max_val+1) for j in range(i,max_val+1)]
    d = [i*mod_val+j for i in range(max_val+1) for j in range(i,max_val+1)]
    min_dom = min(d)
    max_dom = max(d)
    
    # declare variables
    a = intvar(min_dom,max_dom,shape=(rows,cols),name="a")
    a_flat = a.flat

    # Restrict to the values in the domain (d)
    # This is not needed since we restrict the values in
    # the "cardinality count" below.
    # Also, it yield some strange error:
    # AttributeError: 'numpy.bool_' object has no attribute 'is_bool'
    # for i in range(rows):
    #     for j in range(cols):
    #         model += [member_of(d,a[i,j])]
    
    #
    # constraints
    #
    # All possible combinations
    table_accept = [(e,e % mod_val) for e in d ] + [(e,e // mod_val) for e in d]

    for i in range(rows):
        for j in range(cols):
            if problem[i][j] >= 0:
                model += [Table((a[i,j],problem[i][j]), table_accept)]
            model += [form_domino(a,i,j,rows,cols)]


    # Must have exactly 2 occurrences of each number in the domain
    for val in d:
        model += [count(a_flat,val,2)]

    return model

def get_model():
    sicstus111 = [
            [1,4,4,8,2,8,3,2,9,11,10,1,7],
            [7,0,2,8,8,9,11,0,0,10,5,2,0],
            [3,9,2,9,0,1,3,11,8,1,1,7,7],
            [1,4,2,10,0,8,7,2,1,11,0,1,7],
            [0,11,2,9,6,11,9,5,9,6,10,1,7],
            [10,4,9,8,6,5,4,6,10,5,2,7,6],
            [6,6,2,6,6,0,6,3,0,10,5,8,11],
            [4,9,5,3,0,10,7,7,8,2,3,10,3],
            [1,9,0,10,5,7,8,4,9,11,8,8,9],
            [4,4,0,10,11,11,2,10,4,7,5,5,11],
            [3,6,2,1,6,10,4,3,3,5,6,5,7],
            [1,9,3,4,1,5,11,5,3,8,11,3,4]

        ]

    return domino(sicstus111,0)

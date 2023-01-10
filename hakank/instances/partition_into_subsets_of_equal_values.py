"""
Partition into subset of equal sums in cpmpy.

From Programmers Stack Exchange (C#)
http://programmers.stackexchange.com/questions/153184/partitioning-set-into-subsets-with-respect-to-equality-of-sum-among-subsets
Partitioning set into subsets with respect to equality of sum among subsets
'''
let say i have {3, 1, 1, 2, 2, 1,5,2,7} set of numbers, I need to split the 
numbers such that sum of subset1 should be equal to sum of subset2 
{3,2,7} {1,1,2,1,5,2}. First we should identify whether we can split number(one 
way might be dividable by 2 without any remainder) and if we can, we should 
write our algorithm two create s1 and s2 out of s.

How to proceed with this approach? I read partition problem in wiki and even in some 
articles but i am not able to get anything. Can someone help me to find the 
right algorithm and its explanation in simple English?
'''

In my solution to the question I show some possible solutions in MiniZinc and
Google or-tools/C#:
http://programmers.stackexchange.com/a/153215/13955


Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys, math,string
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *


def random_s(max_val,n,num_subsets):
    s = np.random.randint(1,max_val+1,n)
    while sum(s) % num_subsets != 0:
        s[np.random.randint(0,n)] += 1

    return cpm_array(s)
  

def partition_into_subsets_of_equal_values(s,num_subsets,num_sols=0):

    n = len(s)

    partition_sum = sum(s) // num_subsets
    #print("n:",n,"num_subsets:",num_subsets,"partition_sum:",partition_sum)

    # variables
    x = intvar(0,num_subsets-1,shape=n,name="x")

    # constraints
    model = Model([x[0] == 0 # symmetry breaking
                   ])

    for k in range(num_subsets):
        model += [sum([s[i]*(x[i]==k) for i in range(n)]) == partition_sum]

    return model

def get_model(seed=0):
    # A larger random instance
    num_subsets = 3
    max_val = 100
    n = 1000 # 10000
    gen_s = random_s(max_val,n,num_subsets)
    num_sols = 1
    return partition_into_subsets_of_equal_values(gen_s,num_subsets,num_sols)

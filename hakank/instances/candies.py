"""
Candies problem in cpmpy.

From HackerRank
https://www.hackerrank.com/challenges/candies
'''
Alice is a kindergarden teacher. She wants to give some candies to the 
children in her class.  All the children sit in a line and each  of 
them  has a rating score according to his or her usual performance.  
Alice wants to give at least 1 candy for each child.Children get 
jealous of their immediate neighbors, so if two children sit next 
to each other then the one with the higher rating must get more 
candies. Alice wants to save money, so she wants to minimize the 
total number of candies.

Input

The first line of the input is an integer N, the number of children 
in Alice's class. Each of the following N lines contains an integer 
indicates the rating of each child.

Ouput

Output a single line containing the minimum number of candies Alice must give.

Sample Input

3
1
2
2

Sample Ouput

4

Explanation

The number of candies Alice must give are 1, 2 and 1.

Constraints:

N and the rating of each child are no larger than 10^5.
'''



Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my CPMpy page: http://www.hakank.org/cpmpy/

"""
import os,random
from cpmpy import *
import numpy as np
from instances.cpmpy_hakank import *


def candies(input=[1,2,2]):
  n = len(input)


  # variables
  x = intvar(1,n,shape=n,name="x")
  z = intvar(1,n*10**5,name="z")

  # constraints
  model = Model([z == sum(x),
                 z >= n
                 ])

  for i in range(1,n):
    if input[i-1] > input[i]:
      model += (x[i-1] > x[i])
    elif input[i-1] < input[i]:
      model += (x[i-1] < x[i])

  model.minimize(z)

  return model

def get_model(seed=0):
  n = 10**4
  return candies([random.randint(1,n) for i in range(n)])

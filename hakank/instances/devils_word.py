"""
Devil's Word in cpmpy.

i.e. addition/subtraction of an array of numbers to give a specific total (e.g. 666)

Also, see my CGI program 'Devil's Word'
http://www.hakank.org/data_snooping/666.cgi


Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *



def devils_word(total, arr):
  model = Model()

  n = len(arr)
  max_val = max(arr)

  # variables
  plus = boolvar(shape=n,name="plus")   # is the number arr[i] to be added
  minus = boolvar(shape=n,name="minus") # or is it to be subtracted?

  # array with the number with correct sign
  result = intvar(-max_val,max_val,shape=n,name="result")

  # number of minus entries (perhaps to be minimized)
  num_minus = intvar(0,sum(arr),name="num_minus") 

  # constraints
  
  for i in range(n):
    # either plus or minus
    model += [plus[i] + minus[i] == 1]
    # calculate the result array
    model += [result[i] == arr[i]*plus[i] + (-arr[i])*minus[i]]

  # calculate the sum of the numbers in arr
  # model += [total == Sum([arr[i]*plus[i] + (-arr[i])*minus[i] for i in range(n)]))
  model += [total == sum([result[i] for i in range(n)])]

  model += [num_minus == sum([minus[i] == 1 for i in range(n)])]

  return model
 

# My name ("Håkan Kjellerstrand") in ASCII numbers.
# Cf http://www.hakank.org/data_snooping/666.cgi?name=H#E5kan+Kjellerstrand&submit=ok
# which gives the solution:
# +72+229+107+97+110+32+75-106+101+108-108+101-114-115-116-114+97+110+100 = 666
#
# There are 288 different solutions...

def get_model():
  #
  total = 666
  s = "Håkan Kjellerstrand"
  #print("s:", s)
  arr = [ord(c) for c in s]
  # arr = [72, 229, 107, 97, 110, 32, 75, 106, 101, 108, 108, 101, 114, 115, 116, 114, 97, 110, 100]
  return devils_word(total,arr)

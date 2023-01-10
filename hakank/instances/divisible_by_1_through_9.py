"""
Divisible by 1 through 9 puzzle in cpmpy.

http://mindyourdecisions.com/blog/2016/04/10/find-the-10-digit-number-where-n-digits-are-divisible-by-n-sunday-puzzle/
'''
Find a 10 digit number that uses each of the digits 0 to 9 exactly once and 
where the number formed by the first n digits of the number is divisible by n.

You should read the digits of the number from left to right. For example, in the 
number abcd, you need the number a to be divisible by 1, the number ab to be 
divisible by 2, the number abc to be divisible by 3, and the entire number abcd 
to be divisible by 4.
'''


Solution for base=10
x = [3,8,1,6,5,4,7,2,9,0]
t = [3,38,381,3816,38165,381654,3816547,38165472,381654729,3816547290]

I.e. the number is 3816547290.

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my CPMpy page: http://www.hakank.org/cpmpy/

"""
import os,random
from cpmpy import *
import numpy as np
from instances.cpmpy_hakank import *


def divisible_by_1_through_9(base=10):

  model = Model()

  # data
  m = base**base - 1
  n = base - 1
  digits_str = "_0123456789ABCDEFGH"

  #print("\nchecking base:", base,"n:",n, "m:",m)


  # declare variables

  # the digits
  x = intvar(0,base-1,shape=base,name="x")
  # the numbers where t[n] contains the answer
  t = intvar(1,m,shape=base,name="t")

  # constraints
  model += (AllDifferent(x))
  for i in range(1,base+1):
    model += (to_num([x[j] for j in range(i)], t[i-1], base))
    model += (t[i-1] % i == 0)

  return model


# base = 10
# if len(sys.argv) > 1:
#   base = int(sys.argv[1])
# divisible_by_1_through_9(base)
# Print the model as well
def get_model(seed=0):
  import random
  random.seed(seed)
  base= random.choice(b for b in range(3,16))
  return divisible_by_1_through_9(base)

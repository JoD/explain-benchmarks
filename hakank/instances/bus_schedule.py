"""
Bus scheduling in cpmpy.

Problem from Taha "Introduction to Operations Research", page 58.

This is a slightly more general model than Taha's.

The model first finds the optimal value (26) and then shows all
the 145 optimal solutions.

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
from cpmpy import *
from cpmpy.solvers import *
import numpy as np
from instances.cpmpy_hakank import *

def bus_schedule(num_buses_check=0):

    # data
    time_slots = 6
    demands = [8, 10, 7, 12, 4, 4]
    max_num = sum(demands)
    x = intvar(0, max_num,shape=time_slots, name="x")
    num_buses = intvar(0, max_num,name="num_buses")

    if num_buses_check > 0:
        model = Model([num_buses == num_buses_check])
    else:
        model = Model(minimize=num_buses)

    # Constraints
    model += [num_buses >= 0, num_buses == sum(x)]

    # Meet the demands for this and the next time slot
    model += [x[i]+x[i+1] >= demands[i] for i in range(time_slots-1)]

    # The demand "around the clock"
    model += [x[time_slots-1] + x[0] == demands[time_slots-1]]

    return model

def get_model(seed=0):
    return  bus_schedule()

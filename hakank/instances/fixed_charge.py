"""
Fixed-charge problem in cpmpy.

From the OPL documentation, and example model fixed.mod:
'''
Fixed-charge problems are another classic application of integer programs 
(see Applications and Algorithms by W. Winston in the Bibliography). 
They resemble some of the production problems seen previously but differ 
in two respects: the production is an integer value (e.g., a factory 
must produce bikes or toys), and the factories need to rent (or acquire) 
some tools to produce some of the products. Consider the following 
problem. A company manufactures shirts, shorts, and pants. Each 
product requires a number of hours of labor and a certain amount of 
cloth, and the company has a limited capacity of both. In addition, 
all of these products can be manufactured only by renting an appropriate 
machine. The profit on the products (excluding the cost of renting 
the equipment) are also known. The company would like to maximize 
its profit.
'''

Model created by Hakan Kjellerstrand, hakank@hakank.com
See also my cpmpy page: http://www.hakank.org/cpmpy/

"""
import sys,math
import numpy as np
from cpmpy import *
from cpmpy.solvers import *
from instances.cpmpy_hakank import *



def fixed_charge():

    shirtM = 0
    shortM = 1
    pantM = 2
    machines = [shirtM, shortM, pantM]
    num_machines = len(machines)
    
    shirt = 0
    shorts = 1
    pants = 2    
    products = [shirt, shorts, pants]
    num_products = len(products)

    labor = 0
    cloth = 1
    resources = [labor, cloth]
    
    capacity = [ 150, 160 ]
    max_production = max(capacity)
    renting_cost = [ 200, 150, 100 ]


    # profit, producttype
    product = [[6, shirtM],
               [4, shortM],
               [7, pantM]]

    use = [[3,4],
           [2,3],
           [6,4]]

    # variables

    rent = boolvar(shape=num_machines,name="rent")
    produce = intvar(0,max_production,shape=num_products)
    z = intvar(0,10000,name="z")

    model = Model([ z ==
                       sum([product[p][0] * produce[p] for p in products])  -
                       sum([renting_cost[m] * rent[m] for m in machines])
                      ])
    for r in resources:
        model += (sum([use[p][r] * produce[p] for p in products]) <= capacity[r])
                  
        
    for p in products:
        model += (produce[p] <= max_production * rent[p])

    model.maximize(z)
    return model

def get_model(seed=0):
    return fixed_charge()

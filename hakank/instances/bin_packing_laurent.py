"""
Bin packing problem in cpmpy.

This is a fairly faithful port of Laurent Perron's OR-tools CP-SAT model
from https://groups.google.com/g/or-tools-discuss/c/-LfLqZezJ78/m/joeTpWEvAgAJ

This cpmpy model was written by Hakan Kjellerstrand (hakank@gmail.com)
See also my cpmpy page: http://hakank.org/cpmpy/

"""
from cpmpy import *
import numpy as np
from instances.cpmpy_hakank import *

BOX_COEFFICIENT = 10000000
def bin_packing():
    items = {
        1: {'volume': 33, 'weight': 50, 'quantity': 1},
        2: {'volume': 45, 'weight': 30, 'quantity': 1},
        3: {'volume': 10, 'weight': 20, 'quantity': 1},
        4: {'volume': 12, 'weight': 25, 'quantity': 1},
        5: {'volume': 1, 'weight': 2, 'quantity': 1},
        6: {'volume': 22, 'weight': 28, 'quantity': 1},
        7: {'volume': 50, 'weight': 68, 'quantity': 1},
    }

    boxes = {
        1: {'volume': 40, 'weight': 600},
        2: {'volume': 100, 'weight': 1000},
        3: {'volume': 5, 'weight': 1000},
        4: {'volume': 150, 'weight': 500},
        5: {'volume': 120, 'weight': 1000},
    }



    all_items = range(1, len(items) + 1)
    all_boxes = range(1, len(boxes) + 1)

    x = {}
    for i in all_items:
        for j in all_boxes:
            x[(i, j)] = intvar(0, items[i]['quantity'], name='x_%i_%i' % (i, j))

    y = {}
    for j in all_boxes:
        y[j] = boolvar(name='y[%i]' % j)

    model = Model(minimize= sum(y[j] * (BOX_COEFFICIENT + boxes[j]['volume']) for j in all_boxes))
    
    for i in all_items:
        model += (sum(x[i, j] for j in boxes) == items[i]['quantity'])

    for j in all_boxes:
        model += (sum(x[(i, j)] * items[i]['volume'] for i in all_items) <= y[j] * boxes[j]['volume'])
        model += (sum(x[(i, j)] * items[i]['weight'] for i in all_items) <= y[j] * boxes[j]['weight'])

        return model

def get_model():
    return bin_packing()




import random

def generate_packing_problem(n_items, width, seed=0):

    random.seed(seed)

    lb, ub = 1, width

    widths = [random.randint(lb,ub) for _ in range(n_items)]
    heights = [random.randint(lb,ub) for _ in range(n_items)]

    return {"bin_width": width,
            "widths" :widths,
            "heights":heights
            }


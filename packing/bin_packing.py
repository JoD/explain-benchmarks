
import random

def generate_packing_problem(n_items, bin_width, seed=0):

    random.seed(seed)

    lb, ub = 1, bin_width // 2

    widths = [random.randint(lb,ub) for _ in range(n_items)]
    heights = [random.randint(lb,ub) for _ in range(n_items)]

    return {"bin_width": bin_width,
            "widths" :widths,
            "heights":heights
            }


def generate_2d_packing_problem(n_items, seed=0):

    random.seed(seed)

    lb,ub = 1,10

    widths = [random.randint(lb, ub) for _ in range(n_items)]
    heights = [random.randint(lb, ub) for _ in range(n_items)]

    return {"bin_width": sum(widths),
            "widths": widths,
            "heights": heights
            }

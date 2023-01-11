import cpmpy as cp
import copy
from cpmpy.transformations.get_variables import get_variables_model, get_variables
from cpmpy.transformations.flatten_model import flatten_model
import random
import numpy as np

def make_unsat_model(model, p=0.05, max_steps=1):
    """Modify given model to an unsat one while recursing through
    the expressions. The default probability of modifying an expression is
    0.05.

    Args:
        model (cpmpy.Model): CPMpy model.
        p (float, optional): Probability of modifying an expression

    Returns:
        _type_: _description_
    """
    ## Introduce mistakes non-trivially
    ## Random instance selection
    swapping_functions = {
        # "swap_variables_global": swap_variables_global,
        "swap_operator": swap_operator,
        # "swap_indexes_offsets": swap_indexes_offsets, 
        "swap_variables": swap_variables,
        "swap_order_variables": swap_order_variables,
        # "change_constraint": change_constraint,
    }

    all_constraints = model.constraints
    model_variables = get_variables_model(model)
    k=max(1, int(round(p*len(all_constraints))))

    # has_globals = any(isinstance(c, cp.expressions.globalconstraints.GlobalConstraint) for c in all_constraints)

    print("# constraints changed at every iteration=\t", k)
    steps = 0

    while(cp.Model(all_constraints).solve() and steps < max_steps):
        ## 1. Swapping arguments to gloabal
        ## 4. wrong variables in constraints
        ## 2. changing relational operators
        ## 3. Changing indexes ooffsets
        ## 5. Removing negations
        ## 6. Changig constraints
        selected_constraints = set(random.sample(all_constraints, k=k ))
        remaining_constraints = set(all_constraints) - selected_constraints

        print(f"\n\t selected constraints [{len(selected_constraints)}/{len(all_constraints)}]=", "\n\t\t- ".join(str(c) for c in selected_constraints))
        print(f"\n\t remaining constraints [{len(remaining_constraints)}/{len(all_constraints)}]", "\n\t\t- ".join(str(c) for c in remaining_constraints))

        for c in selected_constraints:
            swapping_fun = random.choice(list(swapping_functions))
            swapped_constraint = swapping_functions[swapping_fun](c, model_variables)
            remaining_constraints.add(swapped_constraint)

        all_constraints = list(remaining_constraints)
        steps += 1

    return cp.Model(all_constraints)

def swap_variables_global(expr, variables):
    v = get_variables(expr)
    print("swap_variables_global")
    print("\t- expr", expr)
    return expr

def swap_variables(expr, variables):
    print("swap_variables")
    print("\t- expr", expr)
    return expr

def swap_operator(expr, variables):
    print("swap_operator")
    print("\t- expr", expr)
    
    return expr

def change_constraint(expr, variables):
    print("change_constraint")
    print("\t- expr", expr)
    return expr

def swap_indexes_offsets(expr, variables):
    print("swap_indexes_offsets")
    print("\t- expr", expr)
    return expr

def model_sudoku(dim=9):
  """Generates a Sudoku puzzle for given dimensions, defaults to a 9x9 Sudoku
  puzzle.

  Args:
      dims (tuple, optional): Dimensions of Sudoku Puzzle. Defaults to (9, 9).

  Returns:
      _type_: np.array
  """
  e = 0

  puzzle = cp.intvar(lb=1, ub=dim, shape=(dim, dim), name="cells")
  given = np.zeros(shape=(dim, dim), dtype=int)

  model = cp.Model(
      # Constraints on rows and columns
      [cp.AllDifferent(row) for row in puzzle],
      [cp.AllDifferent(col) for col in puzzle.T], # numpy's Transpose
  )
  # Constraints on blocks
  n = int(dim ** (1/2))
  for i in range(0,dim, n):
      for j in range(0,dim, n):
          model += cp.AllDifferent(puzzle[i:i+n, j:j+n]) # python's indexing

  nsol = model.solveAll(solution_limit=2)
  uniq_solution = puzzle.value()

  givens_cons = (puzzle == uniq_solution)

  remaining_unraveled_indices = list(set(range(dim * dim)))
  remaining_indices = np.random.choice(remaining_unraveled_indices, size=len(remaining_unraveled_indices), replace=False)
  num_taken = 0

  while(nsol > 1):
    unraveld_indices = np.unravel_index([remaining_indices[num_taken]], given.shape)
    con = givens_cons[unraveld_indices]
    given[unraveld_indices] = uniq_solution[unraveld_indices]
    model += con
    nsol = model.solveAll(solution_limit=2)
    num_taken += 1

  return model


if __name__=="__main__":
    sudoku_model = flatten_model(model_sudoku(4))
    make_unsat_model(sudoku_model, p=0.2)
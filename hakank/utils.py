import cpmpy as cp
import copy
from cpmpy.transformations.get_variables import get_variables_model, get_variables
from cpmpy.transformations.flatten_model import flatten_model
import random
import numpy as np

def make_unsat_model(model: cp.Model, p=0.05, max_steps=5):
    """Modify given model to an unsat one while recursing through
    the expressions. The default probability of modifying an expression is
    0.05.

    Args:
        model (cpmpy.Model): CPMpy model.
        p (float, optional): Probability of modifying an expression

    Returns:
        _type_: _description_
    """
    ## Ensure it's a flattened model, easier iteration over constraints
    
    flattened_model = flatten_model(model)

    ## Introduce mistakes non-trivially
    ## Random instance selection
    swapping_functions = {
        # "swap_variables_global": swap_variables_global,
        "swap_operator": swap_operator,
        # "swap_indexes_offsets": swap_indexes_offsets, 
        "swap_variables": swap_variables,
        "shuffle_variables": shuffle_variables,
        # "change_constraint": change_constraint,
    }

    all_constraints = flattened_model.constraints
    model_variables = get_variables_model(flattened_model)
    k=max(1, int(round(p*len(all_constraints))))
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

        for i, c in enumerate(selected_constraints):
            # print("constraint\n\t-input:", c)
            if isinstance(c, cp.expressions.globalconstraints.GlobalConstraint): 
                swapped_constraint = swap_variables(c, model_variables, k=k, p=p)
            # elif 
            else:
                swapping_fun = random.choice(list(swapping_functions))
                swapped_constraint = swapping_functions[swapping_fun](c, model_variables, p=p)

            remaining_constraints.add(swapped_constraint)

            # print("constraint\n\t-swapped:", swapped_constraint)
        all_constraints = list(remaining_constraints)

        steps += 1

    return cp.Model(all_constraints)

def shuffle_variables(expr, variables, p=0.5):
    if not isinstance(expr, (cp.expressions.core.Comparison, cp.expressions.core.Operator)):
        return expr
    if expr.name in ["==", "!=", "wsum"]:
        return swap_operator(expr, variables, p)
    if len(expr.args) > 1:
        random.shuffle(expr.args)
    return expr

def swap_variables(expr, variables, k=1, p=0.5):
    if not isinstance(expr, (cp.expressions.core.Comparison, cp.expressions.core.Operator)):
        return expr

    expr_vars = get_variables(expr)
    if expr.name == "wsum":
        return replace_wsum(expr, variables)

    idx_to_replace = random.sample(list(range(len(expr.args))), min(k, len(expr.args)))

    for id, i in enumerate(idx_to_replace):
        ## get variables of same type
        if isinstance(expr.args[i], (int)):
            v = random.choice(expr_vars)
            val = random.randint(v.lb, v.ub)
            expr.args[i] = val
        ### replace variables
        elif isinstance(expr.args[i], cp.variables._NumVarImpl):
            vars_to_select = [v for v in variables if type(v) == type(expr.args[i])]
            if len(vars_to_select) == 0:
                continue
            var_to_replace = random.choice(vars_to_select)
            expr.args[i] = var_to_replace
        ## not handling expressions
        else:
            expr.args[i] = swap_variables(expr.args[i], variables, k=k, p=p)

    return expr

def is_math_op(expr):
    return expr.name in ["+", "-", "*"]

def replace_math_op(expr):
    all_ops = ["+", "-", "*"]
    all_ops.remove(expr.name)
    expr.name = random.choice(all_ops)
    return expr

def swap_operator(expr, variables, p=0.5):
    if not isinstance(expr, cp.expressions.core.Expression):
        return expr
    if not isinstance(expr, (cp.variables._NumVarImpl)) and any(isinstance(arg, (cp.expressions.core.Comparison, cp.expressions.core.Operator)) for arg in expr.args) and random.random() < p:
        idx = random.randint(0, len(expr.args) - 1)
        expr.args[idx] = swap_operator(expr.args[idx], variables, p)
        return expr

    if is_relational_constraint(expr):
        new_expr = replace_relational_constraint(expr)
    elif is_and_or(expr):
        new_expr = replace_and_or(expr)
    elif is_eq(expr):
        new_expr = replace_eq(expr)
    elif expr.name == "wsum":
        new_expr = replace_wsum(expr, variables)
    elif is_math_op(expr):
        new_expr = replace_math_op(expr)
    elif isinstance(expr, cp.variables.NegBoolView):
        return ~expr
    elif isinstance(expr, cp.variables._BoolVarImpl):
        return expr
    else:
        # print("expr not handled!", expr.name, expr.args)
        new_expr = expr
    return new_expr


def replace_wsum(expr, variables, p=0.5):
    assert expr.name == "wsum", "Ensure it's a wsum"
    expr_weights, expr_vars = expr.args
    for i, v in enumerate(expr_vars):
        if random.random() < p and isinstance(v, cp.variables._IntVarImpl):
            vars_to_select = [vi for vi in variables if type(vi) == v]
            expr_vars[i] = random.choice(vars_to_select)
    return cp.expressions.core.Operator("wsum", [expr_weights, expr_vars])

def is_relational_constraint(expr):
    return expr.name in [">", ">=", "<", "<="]

def replace_relational_constraint(expr):
    all_ops = [">", ">=", "<", "<="]
    all_ops.remove(expr.name)
    expr.name = random.choice(all_ops)
    return expr

def is_and_or(expr):
    return expr.name in ["and", "or", "->"]

def is_eq(expr):
    return expr.name in ["!=", "=="]

def replace_eq(expr):
    expr.name = "!=" if (expr.name == "==") else "=="
    return expr

def replace_and_or(expr):
    all_ops = ["and", "or", "->"]
    all_ops.remove(expr.name)
    expr.name = random.choice(all_ops)
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
    sudoku_model = model_sudoku(9)
    make_unsat_model(sudoku_model, p=0.05)
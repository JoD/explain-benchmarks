import cpmpy as cp
import numpy as np

def difficult_conflict_at(row, col, given, uniq_solution):
    """Generate candidate inconsistencies at a given position.
    Filter out the too obvious inconsistencies."""
    n = int(len(given) ** (0.5))

    if given[row, col] != 0:
        return []

    candidate_values = []
    for v in range(1, len(given)+1):
        if v == uniq_solution[row, col]:
            continue
        # same row or same col
        if v in given[row,:] or v in given[:, col]:
            continue
        # same block
        top_left_row = (row//n)*n
        top_left_col = (col//n)*n

        if v in given[top_left_row:top_left_row+n, top_left_col:top_left_col+n]:
            continue
        candidate_values.append(v)

    return candidate_values

def difficult_conflicts(given, uniq_solution):
    """Generate candidate inconsistencies for each position.
    Filter out the too obvious inconsistencies."""
    position_conflicts = {}

    # 
    n = int(len(given) ** (0.5))
    for i in range(len(given)):
        for j in range(len(given[0])):
            if given[i, j] != 0:
                continue
            candidate_values = []
            for v in range(1, len(given)+1):
                if v == uniq_solution[i, j]:
                    continue
                # same row or same col
                if v in given[i,:] or v in given[:, j]:
                    continue

                top_left_row = (i//n)*n
                top_left_col = (j//n)*n
                if v in given[top_left_row:top_left_row+n, top_left_col:top_left_col+n]:
                    continue
                candidate_values.append(v)

            position_conflicts[(i, j)] = candidate_values

    return position_conflicts


def model_unsat_sudoku(dim=9, total_errors=1, total_extra_givens=1, seed=0):
    # assert dims[0] == dims[1], f"Sudoku should be modeled as a square nrows, ncols=({dims[0]}, {dims[1]})"
    np.random.seed(seed)

    e = 0

    puzzle = cp.intvar(lb=1, ub=dim, shape=(dim,dim))
    given = np.zeros(shape=(dim,dim), dtype=int)

    indices_to_update = np.random.choice(dim*dim, replace=False, size=dim)
    indices = np.unravel_index(indices_to_update, given.shape)

    given[indices] = np.arange(1, dim+1, dtype=int)

    model = cp.Model(
      # Constraints on rows and columns
      (puzzle[given!=e] == given[given!=e]),
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

    remaining_unraveled_indices = list(set(range(dim*dim)) - set(indices_to_update))
    remaining_indices = np.random.choice(remaining_unraveled_indices, size=len(remaining_unraveled_indices), replace=False)

    num_taken = 0
    num_extra_givens = 0

    #
    while(nsol > 1  and num_taken < len(remaining_unraveled_indices) and num_extra_givens < total_extra_givens):
        unraveld_indices = np.unravel_index([remaining_indices[num_taken]], given.shape)
        con = givens_cons[unraveld_indices]
        given[unraveld_indices] = uniq_solution[unraveld_indices]
        model += con
        nsol = model.solveAll(solution_limit=2)

        if nsol == 1:
            num_extra_givens += 1

        num_taken += 1
    sat_sudoku = np.array(given)

    ## adding some errors
    num_errors = 0

    while(num_errors < total_errors and num_taken < len(remaining_unraveled_indices)):
        ##
        
        unraveld_indices = np.unravel_index([remaining_indices[num_taken]], given.shape)
        row, col = unraveld_indices[0][0], unraveld_indices[1][0]
        
        remaining_values = difficult_conflict_at(row, col, given, uniq_solution)

        if len(remaining_values) == 0:
            num_taken += 1
            continue
        
        val = np.random.choice(remaining_values, replace=False, size=1)
        given[unraveld_indices] = val

        num_taken += 1
        num_errors += 1

    return {"givens" :given, "sat": sat_sudoku}

def model_solve_sudoku(dims=(9, 9)):
  """Generates a Sudoku puzzle for given dimensions, defaults to a 9x9 Sudoku
  puzzle.

  Args:
      dims (tuple, optional): Dimensions of Sudoku Puzzle. Defaults to (9, 9).

  Returns:
      _type_: np.array
  """
  assert dims[0] == dims[1], f"Sudoku should be modeled as a square nrows, ncols=({dims[0]}, {dims[1]})"
  e = 0

  puzzle = cp.intvar(lb=1, ub=dims[0], shape=dims)
  given = np.zeros(shape=dims, dtype=int)
  indices_to_update = np.random.choice(dims[1]*dims[0], replace=False, size=dims[0])
  indices = np.unravel_index(indices_to_update, given.shape)

  given[indices] = np.arange(1, dims[0] + 1, dtype=int)

  model = cp.Model(
      # Constraints on rows and columns
      (puzzle[given!=e] == given[given!=e]),
      [cp.AllDifferent(row) for row in puzzle],
      [cp.AllDifferent(col) for col in puzzle.T], # numpy's Transpose
  )
  # Constraints on blocks
  n = int(dims[0] ** (1/2))
  for i in range(0,dims[0], n):
      for j in range(0,dims[1], n):
          model += cp.AllDifferent(puzzle[i:i+n, j:j+n]) # python's indexing

  nsol = model.solveAll(solution_limit=2)
  uniq_solution = puzzle.value()

  givens_cons = (puzzle == uniq_solution)

  remaining_unraveled_indices = list(set(range(dims[1]*dims[0])) - set(indices_to_update))
  remaining_indices = np.random.choice(remaining_unraveled_indices, size=len(remaining_unraveled_indices), replace=False)

  num_taken = 0

  while(nsol > 1):
    unraveld_indices = np.unravel_index([remaining_indices[num_taken]], given.shape)
    con = givens_cons[unraveld_indices]
    given[unraveld_indices] = uniq_solution[unraveld_indices]
    model += con
    nsol = model.solveAll(solution_limit=2)
    num_taken += 1

  return given

if __name__ == "__main__":
  print(model_unsat_sudoku(total_errors=5, total_extra_givens=5))
import cpmpy as cp
import numpy as np



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


print(model_solve_sudoku())
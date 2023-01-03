import cpmpy as cp
import numpy as np

def update_costs_split_value(sat_solver, cells, unsat_given, weights, ocus_costs, base_assum_dict, uniq_solution, assigned_cell=None):
    from CSPExplain.subset.weighted import WeightedOCUS
    from CSPExplain.subset.mus import SMUS
    from CSPExplain.subset.grow import CorrSubsets, GreedyGrow

    n = int(len(unsat_given) ** (0.5))
    if assigned_cell:
        assigned_i, assigned_j = assigned_cell

        all_ij_comb = set()
        for col in range(len(unsat_given)):
            ## all vars on same row
            all_ij_comb.add((assigned_i, col))
            ## all vars on same col
            all_ij_comb.add((col, assigned_j))

        top_left_row = (assigned_i//n)*n
        top_left_col = (assigned_j//n)*n

        for row in range(n):
            for col in range(n):
                all_ij_comb.add((top_left_row+row, top_left_col+col))

    print("\n\n")
    for row in range(len(unsat_given)):
        for col in range(len(unsat_given[0])):
            if unsat_given[row, col] != 0:
                continue

            if assigned_cell and (row, col) not in all_ij_comb:
                continue

            for v in range(1, len(unsat_given)+1):
                print((row, col, v))
                if v == uniq_solution[row, col]:
                    continue

                # introducing the inconsistency
                cpm_cons = cells[row, col] == v
                ind = cp.boolvar(name=f"->{cpm_cons}")

                sat_solver += ind.implies(cpm_cons)

                assum_dict ={**base_assum_dict, **{ind:cpm_cons}}
                                # same row or same col
                top_left_row = (row//n)*n
                top_left_col = (col//n)*n
                if v in unsat_given[row,:] or v in unsat_given[:, col] or v in unsat_given[top_left_row:top_left_row+n, top_left_col:top_left_col+n]:
                    ocus_costs[(row, col, v)] = (ind, cpm_cons, None, 22)
                    continue

                smus_algo = WeightedOCUS(
                    sat_solver=sat_solver,
                    assum_dict=assum_dict,
                    weights= weights + [1], grow_class=CorrSubsets, sub_grow_algo=GreedyGrow,
                    constraint=[ind == 1])

                smus = smus_algo.get_subset()
                smus_cons = [assum_dict[c] for c in smus]
                ocus_cost = sum(20 if isinstance(c, cp.AllDifferent) else 1 for c in smus_cons)
                ocus_costs[(row, col, v)] = (ind, cpm_cons, smus_cons, ocus_cost)
    print("\n\n")


def update_costs_split_var(sat_solver, cells, unsat_given, weights, ocus_costs, base_assum_dict, uniq_solution, assigned_cell=None):
    from CSPExplain.subset.weighted import WeightedOCUS
    from CSPExplain.subset.mus import SMUS
    from CSPExplain.subset.grow import CorrSubsets, GreedyGrow
    
    n = int(len(unsat_given) ** (0.5))
    if assigned_cell:
        assigned_i, assigned_j = assigned_cell
        
        all_ij_comb = set()
        for col in range(len(unsat_given)):
            ## all vars on same row
            all_ij_comb.add((assigned_i, col))
            ## all vars on same col
            all_ij_comb.add((col, assigned_j))

        top_left_row = (assigned_i//n)*n
        top_left_col = (assigned_j//n)*n

        for row in range(n):
            for col in range(n):
                all_ij_comb.add((top_left_row+row, top_left_col+col))

    print("\n\n")
    for row in range(len(unsat_given)):
        for col in range(len(unsat_given[0])):
            if unsat_given[row, col] != 0:
                continue

            if assigned_cell and (row, col) not in all_ij_comb:
                continue

            for v in range(1, len(unsat_given)+1):
                print((row, col, v))
                if v == uniq_solution[row, col]:
                    continue

                # introducing the inconsistency
                cpm_cons = cells[row, col] == v
                ind = cp.boolvar(name=f"->{cpm_cons}")

                sat_solver += ind.implies(cpm_cons)

                assum_dict ={**base_assum_dict, **{ind:cpm_cons}}
                                # same row or same col
                top_left_row = (row//n)*n
                top_left_col = (col//n)*n
                if v in unsat_given[row,:] or v in unsat_given[:, col] or v in unsat_given[top_left_row:top_left_row+n, top_left_col:top_left_col+n]:
                    ocus_costs[(row, col, v)] = (ind, cpm_cons, None, 22)
                    continue

                smus_algo = WeightedOCUS(
                    sat_solver=sat_solver,
                    assum_dict=assum_dict,
                    weights= weights + [1], grow_class=CorrSubsets, sub_grow_algo=GreedyGrow,
                    constraint=[ind == 1])

                smus = smus_algo.get_subset()
                smus_cons = [assum_dict[c] for c in smus]
                ocus_cost = sum(20 if isinstance(c, cp.AllDifferent) else 1 for c in smus_cons)
                ocus_costs[(row, col, v)] = (ind, cpm_cons, smus_cons, ocus_cost)
    print("\n\n")

def update_costs(sat_solver, cells, unsat_given, weights, ocus_costs, base_assum_dict, uniq_solution, assigned_cell=None):
    from CSPExplain.subset.weighted import WeightedOCUS
    from CSPExplain.subset.mus import SMUS
    from CSPExplain.subset.grow import CorrSubsets, GreedyGrow
    
    n = int(len(unsat_given) ** (0.5))
    if assigned_cell:
        assigned_i, assigned_j = assigned_cell
        
        all_ij_comb = set()
        for col in range(len(unsat_given)):
            ## all vars on same row
            all_ij_comb.add((assigned_i, col))
            ## all vars on same col
            all_ij_comb.add((col, assigned_j))

        top_left_row = (assigned_i//n)*n
        top_left_col = (assigned_j//n)*n

        for row in range(n):
            for col in range(n):
                all_ij_comb.add((top_left_row+row, top_left_col+col))

    print("\n\n")
    for row in range(len(unsat_given)):
        for col in range(len(unsat_given[0])):
            if unsat_given[row, col] != 0:
                continue

            if assigned_cell and (row, col) not in all_ij_comb:
                continue

            for v in range(1, len(unsat_given)+1):
                print((row, col, v))
                if v == uniq_solution[row, col]:
                    continue

                # introducing the inconsistency
                cpm_cons = cells[row, col] == v
                ind = cp.boolvar(name=f"->{cpm_cons}")

                sat_solver += ind.implies(cpm_cons)

                assum_dict ={**base_assum_dict, **{ind:cpm_cons}}
                                # same row or same col
                top_left_row = (row//n)*n
                top_left_col = (col//n)*n
                if v in unsat_given[row,:] or v in unsat_given[:, col] or v in unsat_given[top_left_row:top_left_row+n, top_left_col:top_left_col+n]:
                    ocus_costs[(row, col, v)] = (ind, cpm_cons, None, 22)
                    continue

                smus_algo = WeightedOCUS(
                    sat_solver=sat_solver,
                    assum_dict=assum_dict,
                    weights= weights + [1], grow_class=CorrSubsets, sub_grow_algo=GreedyGrow,
                    constraint=[ind == 1])

                smus = smus_algo.get_subset()
                smus_cons = [assum_dict[c] for c in smus]
                ocus_cost = sum(20 if isinstance(c, cp.AllDifferent) else 1 for c in smus_cons)
                ocus_costs[(row, col, v)] = (ind, cpm_cons, smus_cons, ocus_cost)
    print("\n\n")

def ocus_conflict(given, uniq_solution, num_errors=1):
    from CSPExplain.examples.sudoku import build_all_sudoku_constraints

    errors_added = 0
    unsat_given = np.array(given)
    sudoku_constraints, cells = build_all_sudoku_constraints(unsat_given)
    weights = [20 if isinstance(cpm_cons, cp.AllDifferent) else 1 for cpm_cons in sudoku_constraints]

    num_unassigned = len(unsat_given[unsat_given == 0])
    sat_solver = cp.SolverLookup.get("pysat")

    base_assum_dict = {}
    for cpm_cons in sudoku_constraints:
        ind = cp.boolvar(name=f"->{cpm_cons}")
        sat_solver += ind.implies(cpm_cons)
        base_assum_dict[ind] = cpm_cons

    ocus_costs = {}

    ### do it incremnetally !
    update_costs(sat_solver, cells, unsat_given, weights, ocus_costs, base_assum_dict, uniq_solution)

    while errors_added < num_errors and errors_added < num_unassigned:
        (i, j, v) = max(ocus_costs, key=lambda x: ocus_costs[x][3])
        (ind, cpm_cons, _, _) = ocus_costs[(i, j, v)]

        for vij in range(1, len(unsat_given)+1):
            if vij == uniq_solution[i, j]:
                continue
            del ocus_costs[i, j, vij]

        unsat_given[i, j] = v
        weights += [1]
        errors_added += 1

        ## recompute ocus_costs
        base_assum_dict[ind] = cpm_cons
        ocus_errors_only = np.array(unsat_given)
        ocus_errors_only[given == unsat_given] = 0

        ### do it incremnetally !
        update_costs(sat_solver, cells, unsat_given, weights, ocus_costs, base_assum_dict, uniq_solution, assigned_cell=(i, j))

    return unsat_given

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
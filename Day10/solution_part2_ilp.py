#!/usr/bin/env python3

import sys
from typing import List, Tuple

# Try to import various ILP solvers in order of preference
ORTOOLS_AVAILABLE = False
PULP_AVAILABLE = False
CVXPY_AVAILABLE = False

try:
    from ortools.linear_solver import pywraplp
    ORTOOLS_AVAILABLE = True
except ImportError:
    pass

try:
    import pulp
    PULP_AVAILABLE = True
except ImportError:
    pass

try:
    import cvxpy as cp
    CVXPY_AVAILABLE = True
except ImportError:
    pass

if not any([ORTOOLS_AVAILABLE, PULP_AVAILABLE, CVXPY_AVAILABLE]):
    print("Warning: No ILP solvers available. Install ortools, pulp, or cvxpy.")
    print("Falling back to basic bounded search.")

def parse_machine_part2(line: str) -> Tuple[List[List[int]], List[int]]:
    """Parse a single machine line for Part 2 - extract buttons and joltage targets."""
    parts = line.strip().split()
    
    # Find button parts (in parentheses) and joltage part (in curly braces)
    button_parts = []
    joltage_part = None
    
    for part in parts:
        if part.startswith('(') and part.endswith(')'):
            button_parts.append(part)
        elif part.startswith('{') and part.endswith('}'):
            joltage_part = part
    
    # Parse buttons: (3) -> [3], (1,3) -> [1,3]
    buttons = []
    for button_part in button_parts:
        button_str = button_part[1:-1]  # Remove parentheses
        if button_str:
            button_indices = [int(x) for x in button_str.split(',')]
            buttons.append(button_indices)
        else:
            buttons.append([])
    
    # Parse joltage targets: {3,5,4,7} -> [3,5,4,7]
    joltage_str = joltage_part[1:-1]  # Remove braces
    targets = [int(x) for x in joltage_str.split(',')]
    
    return buttons, targets

def solve_machine_ilp_ortools(buttons: List[List[int]], targets: List[int]) -> int:
    """Solve using OR-Tools Integer Linear Programming."""
    n = len(targets)  # number of counters
    m = len(buttons)  # number of buttons

    # Create solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        # Fallback to CBC if SCIP is not available
        solver = pywraplp.Solver.CreateSolver('CBC')
        if not solver:
            return None  # Solver not available

    # Create variables: x[j] = number of times to press button j
    x = [solver.IntVar(0, solver.infinity(), f'x_{j}') for j in range(m)]

    # Add constraints: for each counter i, sum of presses affecting it equals target[i]
    for i in range(n):
        constraint = solver.Constraint(targets[i], targets[i])
        for j, button in enumerate(buttons):
            if i in button:
                constraint.SetCoefficient(x[j], 1)

    # Objective: minimize total presses
    objective = solver.Objective()
    for j in range(m):
        objective.SetCoefficient(x[j], 1)
    objective.SetMinimization()

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        return int(solver.Objective().Value())
    else:
        return -1  # No solution found

def solve_machine_ilp_pulp(buttons: List[List[int]], targets: List[int]) -> int:
    """Solve using PuLP Integer Linear Programming."""
    n = len(targets)  # number of counters
    m = len(buttons)  # number of buttons

    # Create the problem
    prob = pulp.LpProblem("ButtonPresses", pulp.LpMinimize)

    # Create variables: x[j] = number of times to press button j
    x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Integer') for j in range(m)]

    # Objective: minimize total presses
    prob += pulp.lpSum(x)

    # Add constraints: for each counter i, sum of presses affecting it equals target[i]
    for i in range(n):
        prob += pulp.lpSum(x[j] for j, button in enumerate(buttons) if i in button) == targets[i]

    # Solve
    status = prob.solve()

    if status == 1:  # Optimal
        return int(pulp.value(prob.objective))
    else:
        return -1  # No solution found

def solve_machine_ilp_cvxpy(buttons: List[List[int]], targets: List[int]) -> int:
    """Solve using CVXPY Integer Linear Programming."""
    n = len(targets)  # number of counters
    m = len(buttons)  # number of buttons

    # Create variables: x[j] = number of times to press button j
    x = cp.Variable(m, integer=True)

    # Build constraint matrix A: n x m (counters x buttons)
    A = []
    for i in range(n):
        row = [1 if i in button else 0 for button in buttons]
        A.append(row)
    A = cp.vstack(A) if A else cp.vstack([])

    # Objective: minimize total presses
    objective = cp.Minimize(cp.sum(x))

    # Constraints: A @ x == targets and x >= 0
    constraints = [A @ x == targets, x >= 0]

    # Solve
    prob = cp.Problem(objective, constraints)
    result = prob.solve()

    if prob.status == cp.OPTIMAL:
        return int(result)
    else:
        return -1  # No solution found

def solve_machine_bounded_bfs(buttons: List[List[int]], targets: List[int]) -> int:
    """Fallback bounded BFS solver."""
    from collections import deque

    n = len(targets)
    m = len(buttons)

    start_state = tuple([0] * n)
    target_state = tuple(targets)

    queue = deque([(start_state, 0, [0] * m)])
    visited = set([start_state])
    best_cost = float('inf')

    max_presses = 200  # Reasonable limit for fallback

    while queue:
        current_state, presses, press_counts = queue.popleft()

        if current_state == target_state:
            best_cost = min(best_cost, presses)
            continue

        if presses >= best_cost or presses >= max_presses:
            continue

        for button_idx, button in enumerate(buttons):
            if press_counts[button_idx] >= max_presses // m:  # Distribute limit
                continue

            new_state = list(current_state)
            valid = True

            for counter_idx in button:
                if counter_idx < n:
                    new_state[counter_idx] += 1
                    if new_state[counter_idx] > targets[counter_idx]:
                        valid = False
                        break

            if not valid:
                continue

            new_state_tuple = tuple(new_state)
            new_press_counts = press_counts[:]
            new_press_counts[button_idx] += 1

            if new_state_tuple not in visited:
                visited.add(new_state_tuple)
                queue.append((new_state_tuple, presses + 1, new_press_counts))

    return best_cost if best_cost != float('inf') else -1

def solve_machine_ilp(buttons: List[List[int]], targets: List[int]) -> int:
    """Solve using Integer Linear Programming with multiple solver fallbacks.

    Variables: x_j = number of times to press button j
    Constraints: For each counter i, sum(button_j affects i) * x_j = target[i]
    Objective: minimize sum(x_j)
    """
    # Try solvers in order of preference
    if ORTOOLS_AVAILABLE:
        result = solve_machine_ilp_ortools(buttons, targets)
        if result is not None:
            return result

    if PULP_AVAILABLE:
        result = solve_machine_ilp_pulp(buttons, targets)
        if result != -1:
            return result

    if CVXPY_AVAILABLE:
        result = solve_machine_ilp_cvxpy(buttons, targets)
        if result != -1:
            return result

    # Final fallback
    print("Warning: Using bounded BFS fallback - results may be slow or incomplete")
    return solve_machine_bounded_bfs(buttons, targets)

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()
    
    total_presses = 0
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        
        buttons, targets = parse_machine_part2(line)
        min_presses = solve_machine_ilp(buttons, targets)
        
        if min_presses == -1:
            print(f"Machine {line_num}: No solution found")
        else:
            total_presses += min_presses
            print(f"Machine {line_num}: {min_presses} presses")
    
    print(f"\nTotal minimum presses: {total_presses}")

if __name__ == "__main__":
    main()




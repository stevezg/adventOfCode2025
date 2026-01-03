#!/usr/bin/env python3

import sys
from typing import List, Tuple, Optional

try:
    from ortools.linear_solver import pywraplp
    HAS_ORTOOLS = True
except ImportError:
    HAS_ORTOOLS = False
    print("Warning: OR-Tools not available, falling back to branch-and-bound/BFS methods")

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

def solve_machine_ilp(buttons: List[List[int]], targets: List[int]) -> int:
    """Solve using Integer Linear Programming with OR-Tools."""
    if not HAS_ORTOOLS:
        return solve_machine_part2_fallback(buttons, targets)

    n = len(targets)  # number of counters
    m = len(buttons)  # number of buttons

    # Create solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        # Fallback to CBC if SCIP is not available
        solver = pywraplp.Solver.CreateSolver('CBC')
        if not solver:
            print("Warning: No ILP solver available, using branch-and-bound/BFS methods")
            return solve_machine_part2_fallback(buttons, targets)

    # Create variables: x[j] = number of times to press button j
    x = [solver.IntVar(0, solver.infinity(), f'x_{j}') for j in range(m)]

    # Add constraints: for each counter i, sum(button_j affects i) * x_j = targets[i]
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

def solve_machine_part2_fallback(buttons: List[List[int]], targets: List[int]) -> int:
    """Fallback solver - try branch and bound first, fallback to optimized BFS."""
    # Try branch and bound first (better for large problems)
    result = solve_machine_branch_bound(buttons, targets)

    # If branch and bound fails or is too slow, fallback to optimized BFS
    if result == -1:
        result = solve_machine_optimized_bfs(buttons, targets)

    return result

def solve_machine_branch_bound(buttons: List[List[int]], targets: List[int]) -> int:
    """Solve using branch-and-bound algorithm.
    
    We use a DFS with bounds:
    - Lower bound: ceil(max(target[i] / max_affects[i])) where max_affects[i] is the max
      number of buttons that affect counter i
    - Upper bound: current best solution
    """
    n = len(targets)  # number of counters
    m = len(buttons)  # number of buttons
    
    # Build matrix: effect[i][j] = 1 if button j affects counter i, else 0
    effect = [[0] * m for _ in range(n)]
    for j, button in enumerate(buttons):
        for i in button:
            if i < n:
                effect[i][j] = 1
    
    # Calculate max buttons affecting each counter (for lower bound)
    max_affects = [sum(effect[i]) for i in range(n)]
    
    # Lower bound: for each counter, we need at least ceil(target[i] / max_affects[i]) presses
    # Actually, a better lower bound is the maximum over counters of ceil(target[i] / max_affects[i])
    # But max_affects[i] might be 0, so we need to handle that
    lower_bound = 0
    for i in range(n):
        if max_affects[i] > 0:
            lower_bound = max(lower_bound, (targets[i] + max_affects[i] - 1) // max_affects[i])
        elif targets[i] > 0:
            return -1  # Impossible: counter i needs value but no button affects it
    
    best_solution = None
    best_cost = float('inf')
    
    def apply_button(state: List[int], button_idx: int) -> Optional[List[int]]:
        """Apply button press, return new state or None if invalid."""
        new_state = state[:]
        for counter_idx in buttons[button_idx]:
            if counter_idx < n:
                new_state[counter_idx] += 1
                if new_state[counter_idx] > targets[counter_idx]:
                    return None  # Exceeded target
        return new_state
    
    def branch_bound(presses: List[int], state: List[int], cost: int):
        """Branch and bound recursive function."""
        nonlocal best_solution, best_cost
        
        # Check if we've reached the target
        if state == targets:
            if cost < best_cost:
                best_cost = cost
                best_solution = presses[:]
            return
        
        # Prune if we can't improve
        if cost >= best_cost:
            return
        
        # Calculate a lower bound for remaining presses needed
        remaining = [targets[i] - state[i] for i in range(n)]
        
        # Check if any counter is impossible to reach
        for i in range(n):
            if remaining[i] < 0:
                return
            if remaining[i] > 0 and max_affects[i] == 0:
                return  # Can't increase this counter
        
        # Estimate lower bound for remaining
        remaining_lb = 0
        for i in range(n):
            if remaining[i] > 0 and max_affects[i] > 0:
                # Need at least ceil(remaining[i] / max_affects[i]) more presses
                remaining_lb = max(remaining_lb, (remaining[i] + max_affects[i] - 1) // max_affects[i])
        
        if cost + remaining_lb >= best_cost:
            return  # Prune
        
        # Try each button
        for j in range(m):
            new_state = apply_button(state, j)
            if new_state is not None:
                presses.append(j)
                branch_bound(presses, new_state, cost + 1)
                presses.pop()
    
    # Start with all zeros
    initial_state = [0] * n
    branch_bound([], initial_state, 0)
    
    return int(best_cost) if best_cost != float('inf') else -1

def solve_machine_optimized_bfs(buttons: List[List[int]], targets: List[int]) -> int:
    """Solve using optimized BFS with better state representation and pruning."""
    from collections import deque
    
    n = len(targets)  # number of counters
    m = len(buttons)  # number of buttons
    
    # Start from all zeros
    start_state = tuple([0] * n)
    target_state = tuple(targets)
    
    # BFS queue: (current_state, presses_used)
    queue = deque([(start_state, 0)])
    visited = {start_state: 0}
    
    while queue:
        current_state, presses = queue.popleft()
        
        if current_state == target_state:
            return presses
        
        # Try pressing each button
        for button in buttons:
            new_state_list = list(current_state)
            valid = True
            
            # Apply button press
            for counter_idx in button:
                if counter_idx < n:
                    new_state_list[counter_idx] += 1
                    # Prune if we exceed the target
                    if new_state_list[counter_idx] > targets[counter_idx]:
                        valid = False
                        break
            
            if not valid:
                continue
            
            new_state = tuple(new_state_list)
            
            # Only add if we haven't seen this state or found a better path
            if new_state not in visited or visited[new_state] > presses + 1:
                visited[new_state] = presses + 1
                queue.append((new_state, presses + 1))
    
    return -1  # No solution found

def solve_machine_part2(buttons: List[List[int]], targets: List[int]) -> int:
    """Main solver - uses ILP by default, falls back to branch-and-bound/BFS."""
    return solve_machine_ilp(buttons, targets)

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
        min_presses = solve_machine_part2(buttons, targets)
        
        if min_presses == -1:
            print(f"Machine {line_num}: No solution found")
        else:
            total_presses += min_presses
            if len(lines) <= 10:  # Only print details for small inputs
                print(f"Machine {line_num}: {min_presses} presses")
    
    print(f"Total minimum presses: {total_presses}")

if __name__ == "__main__":
    main()


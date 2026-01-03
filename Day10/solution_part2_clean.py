#!/usr/bin/env python3
"""
Day 10 Part 2: Factory - Joltage Configuration
Find minimum button presses to reach target joltage levels.
Uses Integer Linear Programming for optimal performance on large inputs.
"""

import sys
from typing import List, Tuple

try:
    from ortools.linear_solver import pywraplp
    HAS_ORTOOLS = True
except ImportError:
    HAS_ORTOOLS = False
    print("Warning: OR-Tools not available, falling back to DFS method")


def parse_line(line: str) -> Tuple[List[List[int]], List[int]]:
    """Parse a machine line to extract buttons and joltage targets."""
    parts = line.strip().split()
    
    buttons = []
    joltage_targets = None
    
    for part in parts:
        if part.startswith('(') and part.endswith(')'):
            button_str = part[1:-1]
            buttons.append([int(x) for x in button_str.split(',')] if button_str else [])
        elif part.startswith('{') and part.endswith('}'):
            joltage_targets = [int(x) for x in part[1:-1].split(',')]
    
    return buttons, joltage_targets


def solve_part2_ilp(buttons: List[List[int]], targets: List[int]) -> int:
    """Solve Part 2 using Integer Linear Programming with OR-Tools."""
    if not HAS_ORTOOLS:
        return solve_part2_dfs(buttons, targets)

    n = len(targets)  # number of counters
    m = len(buttons)  # number of buttons

    # Create solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        # Fallback to CBC if SCIP is not available
        solver = pywraplp.Solver.CreateSolver('CBC')
        if not solver:
            print("Warning: No ILP solver available, using DFS method")
            return solve_part2_dfs(buttons, targets)

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

def solve_part2_dfs(buttons: List[List[int]], targets: List[int]) -> int:
    """Solve Part 2 using branch-and-bound DFS (fallback method)."""
    n = len(targets)

    # Build max_affects: max number of buttons affecting each counter
    max_affects = [0] * n
    for button in buttons:
        for counter_idx in button:
            if counter_idx < n:
                max_affects[counter_idx] += 1

    # Check if solution is possible
    for i in range(n):
        if targets[i] > 0 and max_affects[i] == 0:
            return -1

    def lower_bound(state: List[int]) -> int:
        """Calculate lower bound on remaining presses needed."""
        lb = 0
        for i in range(n):
            remaining = targets[i] - state[i]
            if remaining > 0:
                if max_affects[i] == 0:
                    return float('inf')
                # Need at least ceil(remaining / max_affects[i]) presses
                lb = max(lb, (remaining + max_affects[i] - 1) // max_affects[i])
        return lb

    best_cost = float('inf')

    def dfs(state: List[int], cost: int):
        """DFS with branch-and-bound pruning."""
        nonlocal best_cost

        # Check if we've reached the target
        if state == targets:
            best_cost = min(best_cost, cost)
            return

        # Prune if we can't improve
        if cost >= best_cost:
            return

        # Calculate lower bound for remaining
        remaining_lb = lower_bound(state)
        if cost + remaining_lb >= best_cost:
            return

        # Try each button (prioritize buttons that help most)
        button_scores = []
        for j, button in enumerate(buttons):
            score = 0
            for counter_idx in button:
                if counter_idx < n:
                    remaining = targets[counter_idx] - state[counter_idx]
                    if remaining > 0:
                        score += remaining
            button_scores.append((score, j))

        button_order = [j for _, j in sorted(button_scores, reverse=True)]

        for j in button_order:
            new_state = state[:]
            valid = True

            # Apply button press
            for counter_idx in buttons[j]:
                if counter_idx < n:
                    new_state[counter_idx] += 1
                    if new_state[counter_idx] > targets[counter_idx]:
                        valid = False
                        break

            if not valid:
                continue

            # Recursively explore
            dfs(new_state, cost + 1)

    # Start DFS from initial state
    initial_state = [0] * n
    dfs(initial_state, 0)

    return int(best_cost) if best_cost != float('inf') else -1

def solve_part2(buttons: List[List[int]], targets: List[int]) -> int:
    """Main solve function - uses ILP by default, falls back to DFS."""
    return solve_part2_ilp(buttons, targets)


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    
    if input_file:
        with open(input_file, 'r') as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()
    
    total_presses = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        buttons, targets = parse_line(line)
        min_presses = solve_part2(buttons, targets)
        
        if min_presses == -1:
            print(f"Error: No solution found", file=sys.stderr)
            continue
        
        total_presses += min_presses
    
    print(f"Part 2 answer: {total_presses}")


if __name__ == "__main__":
    main()

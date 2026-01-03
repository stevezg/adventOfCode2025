#!/usr/bin/env python3

import sys
from typing import List, Tuple
import heapq

try:
    from ortools.linear_solver import pywraplp
    HAS_ORTOOLS = True
except ImportError:
    HAS_ORTOOLS = False
    print("Warning: OR-Tools not available, falling back to Dijkstra method")

def parse_machine_part2(line: str) -> Tuple[List[List[int]], List[int]]:
    """Parse a single machine line for Part 2 - extract buttons and joltage targets."""
    # Split the line into parts
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
        if button_str:  # Handle empty buttons
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
        return solve_machine_part2_dijkstra(buttons, targets)

    n = len(targets)  # number of counters
    m = len(buttons)  # number of buttons

    # Create solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        # Fallback to CBC if SCIP is not available
        solver = pywraplp.Solver.CreateSolver('CBC')
        if not solver:
            print("Warning: No ILP solver available, using Dijkstra method")
            return solve_machine_part2_dijkstra(buttons, targets)

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

def solve_machine_part2_dijkstra(buttons: List[List[int]], targets: List[int]) -> int:
    """Solve for minimum button presses for Part 2 using Dijkstra (priority queue) - fallback."""
    n = len(targets)  # number of counters
    m = len(buttons)  # number of buttons

    # Start from all zeros
    start_state = tuple([0] * n)
    target_state = tuple(targets)

    # Priority queue: (cost, state)
    pq = [(0, start_state)]
    visited = set([start_state])
    min_cost = {start_state: 0}

    while pq:
        cost, current_state = heapq.heappop(pq)

        if current_state == target_state:
            return cost

        # Try pressing each button
        for button_idx, button in enumerate(buttons):
            new_state = list(current_state)
            valid = True

            # Apply button press
            for counter_idx in button:
                if counter_idx < n:
                    new_state[counter_idx] += 1
                    # Prune if we exceed the target
                    if new_state[counter_idx] > targets[counter_idx]:
                        valid = False
                        break

            if not valid:
                continue

            new_state_tuple = tuple(new_state)
            new_cost = cost + 1

            if new_state_tuple not in min_cost or new_cost < min_cost[new_state_tuple]:
                min_cost[new_state_tuple] = new_cost
                heapq.heappush(pq, (new_cost, new_state_tuple))

    # If we reach here, no solution found
    return -1

def main():
    # Read input from stdin or file
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    total_presses = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        buttons, targets = parse_machine_part2(line)
        min_presses = solve_machine_ilp(buttons, targets)
        total_presses += min_presses
        print(f"Machine {len(targets)} counters, {len(buttons)} buttons: {min_presses} presses")

    print(f"Total minimum presses: {total_presses}")

if __name__ == "__main__":
    main()

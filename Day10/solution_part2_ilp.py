#!/usr/bin/env python3

import sys
from typing import List, Tuple
from ortools.linear_solver import pywraplp

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
    """Solve using Integer Linear Programming.
    
    Variables: x_j = number of times to press button j
    Constraints: For each counter i, sum(button_j affects i) * x_j = target[i]
    Objective: minimize sum(x_j)
    """
    n = len(targets)  # number of counters
    m = len(buttons)  # number of buttons
    
    # Create solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        # Fallback to CBC if SCIP is not available
        solver = pywraplp.Solver.CreateSolver('CBC')
        if not solver:
            raise RuntimeError('No ILP solver available')
    
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
        total_presses = int(solver.Objective().Value())
        return total_presses
    else:
        return -1  # No solution found

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




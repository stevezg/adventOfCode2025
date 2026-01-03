#!/usr/bin/env python3

import sys
from typing import List, Tuple
from copy import deepcopy

def parse_machine(line: str) -> Tuple[List[int], List[List[int]]]:
    """Parse a single machine line into target configuration and button configurations."""
    # Split the line into parts
    parts = line.strip().split()

    # Find the indicator lights part (in brackets)
    indicator_part = None
    button_parts = []
    joltage_part = None

    for part in parts:
        if part.startswith('[') and part.endswith(']'):
            indicator_part = part
        elif part.startswith('(') and part.endswith(')'):
            button_parts.append(part)
        elif part.startswith('{') and part.endswith('}'):
            joltage_part = part

    # Parse indicator lights: [.##.] -> [0, 1, 1, 0]
    lights_str = indicator_part[1:-1]  # Remove brackets
    target = [1 if c == '#' else 0 for c in lights_str]

    # Parse buttons: (3) -> [3], (1,3) -> [1,3]
    buttons = []
    for button_part in button_parts:
        button_str = button_part[1:-1]  # Remove parentheses
        if button_str:  # Handle empty buttons
            button_indices = [int(x) for x in button_str.split(',')]
            buttons.append(button_indices)
        else:
            buttons.append([])

    return target, buttons

def gaussian_elimination_gf2(A: List[List[int]], b: List[int]) -> Tuple[List[int], bool]:
    """
    Solve A x = b over GF(2) using Gaussian elimination.
    A is n x m matrix (n equations, m variables), b is n-vector, x is m-vector.
    Returns (solution, is_consistent). Note: may not be minimum weight.
    """
    n, m = len(A), len(A[0]) if A else 0
    if n == 0 or m == 0:
        return [], len(b) == 0 or all(x == 0 for x in b)

    # A is n x m (n equations, m variables)
    # We want to solve A x = b

    # Create augmented matrix [A | b] which is n x (m+1)
    matrix = [row[:] + [b[i]] for i, row in enumerate(A)]

    # Forward elimination to get row echelon form
    pivot_cols = []
    for col in range(min(n, m)):
        # Find pivot row for this column
        pivot_row = None
        for row in range(col, n):
            if matrix[row][col] == 1:
                pivot_row = row
                break

        if pivot_row is None:
            continue

        # Swap rows to bring pivot to current position
        matrix[col], matrix[pivot_row] = matrix[pivot_row], matrix[col]
        pivot_cols.append(col)

        # Eliminate below
        for row in range(col + 1, n):
            if matrix[row][col] == 1:
                for j in range(m + 1):
                    matrix[row][j] ^= matrix[col][j]

    # Check consistency
    rank = len(pivot_cols)
    for row in range(rank, n):
        if matrix[row][-1] == 1:
            return [], False  # Inconsistent

    # Back substitution to find solution
    x = [0] * m

    for i in range(rank - 1, -1, -1):
        pivot_col = pivot_cols[i]
        sum_val = matrix[i][-1]
        for j in range(pivot_col + 1, m):
            sum_val ^= (matrix[i][j] * x[j])
        x[pivot_col] = sum_val

    return x, True

def solve_machine_gaussian(target: List[int], buttons: List[List[int]]) -> int:
    """Solve for minimum button presses using Gaussian elimination over GF(2)."""
    n = len(target)  # number of lights
    m = len(buttons)  # number of buttons

    if m == 0:
        return 0 if all(t == 0 for t in target) else -1

    # Create matrix A as n x m (n equations for lights, m variables for buttons)
    # Each column represents a button's effect on all lights
    A = [[0] * m for _ in range(n)]
    for j, button in enumerate(buttons):
        for light_idx in button:
            if light_idx < n:
                A[light_idx][j] = 1

    # Solve A x = target over GF(2), where x is the solution vector
    solution, consistent = gaussian_elimination_gf2(A, target)

    if not consistent:
        return -1  # No solution

    # Count the number of presses (number of 1's in solution)
    # Note: This may not be the minimum weight solution
    return sum(solution)

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

        target, buttons = parse_machine(line)
        min_presses = solve_machine_gaussian(target, buttons)
        if min_presses == -1:
            print(f"Machine {len(target)} lights, {len(buttons)} buttons: No solution found!")
            continue
        total_presses += min_presses
        print(f"Machine {len(target)} lights, {len(buttons)} buttons: {min_presses} presses")

    print(f"Total minimum presses: {total_presses}")

if __name__ == "__main__":
    main()

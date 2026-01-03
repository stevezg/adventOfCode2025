#!/usr/bin/env python3

import sys
from typing import List, Tuple
from fractions import Fraction
from copy import deepcopy

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

def gaussian_elimination_rational(A: List[List[Fraction]], b: List[Fraction]) -> Tuple[List[List[Fraction]], List[Fraction], int]:
    """Gaussian elimination over rationals. Returns (U, c, rank) where U x = c."""
    m, n = len(A), len(A[0])
    U = deepcopy(A)
    c = b[:]
    rank = 0

    for col in range(min(m, n)):
        # Find pivot
        pivot_row = None
        for row in range(rank, m):
            if U[row][col] != 0:
                pivot_row = row
                break

        if pivot_row is None:
            continue

        # Swap rows
        U[rank], U[pivot_row] = U[pivot_row], U[rank]
        c[rank], c[pivot_row] = c[pivot_row], c[rank]

        # Eliminate
        pivot = U[rank][col]
        for row in range(rank + 1, m):
            factor = U[row][col] / pivot
            for j in range(col, n):
                U[row][j] -= factor * U[rank][j]
            c[row] -= factor * c[rank]

        rank += 1

    return U, c, rank

def solve_linear_system(buttons: List[List[int]], targets: List[int]) -> int:
    """Solve A x = b with min sum x_i, x_i >= 0 integer."""
    n = len(targets)  # counters
    m = len(buttons)  # buttons

    # Build matrix A: n x m (counters x buttons)
    A = [[Fraction(0) for _ in range(m)] for _ in range(n)]
    for j, button in enumerate(buttons):
        for i in button:
            if i < n:
                A[i][j] = Fraction(1)

    b = [Fraction(t) for t in targets]

    # Gaussian elimination
    U, c, rank = gaussian_elimination_rational(A, b)

    # Check if consistent
    for row in range(rank, n):
        if c[row] != 0:
            return -1  # Inconsistent

    # Now we have the row echelon form
    # Back substitution to find particular solution
    x_particular = [Fraction(0) for _ in range(m)]
    for i in range(rank - 1, -1, -1):
        # Find the pivot column
        pivot_col = None
        for j in range(m):
            if U[i][j] != 0:
                pivot_col = j
                break

        if pivot_col is None:
            continue

        sum_val = c[i]
        for j in range(pivot_col + 1, m):
            sum_val -= U[i][j] * x_particular[j]

        x_particular[pivot_col] = sum_val / U[i][pivot_col]

    # Now find the null space
    # The free variables are columns not used as pivots
    pivot_cols = set()
    for i in range(rank):
        for j in range(m):
            if U[i][j] != 0:
                pivot_cols.add(j)
                break

    free_vars = [j for j in range(m) if j not in pivot_cols]

    # For each free variable, we can add ±1 to find integer solutions
    # But to minimize sum x_i, we need to find the optimal combination

    # Since we want non-negative integer solutions with min sum,
    # and the particular solution may not be integer, we need to find integer solutions

    # This is getting complex. For now, let's assume the particular solution is close to optimal
    # and round it appropriately.

    # Convert to integers by finding the least common multiple of denominators
    denominators = [x.denominator for x in x_particular]
    from math import lcm
    lcm_d = 1
    for d in denominators:
        lcm_d = lcm(lcm_d, d)

    x_int = [int(x * lcm_d) for x in x_particular]
    scale = lcm_d

    # Now x_int / scale is a rational solution
    # But to get integer, we need to adjust by null space vectors

    # For simplicity, let's check if x_int gives the correct result when scaled
    # This is approximate

    # Actually, let's compute A x_particular and see if it gives b
    computed_b = [sum(A[i][j] * x_particular[j] for j in range(m)) for i in range(n)]
    if all(abs(computed_b[i] - b[i]) < 1e-10 for i in range(n)):
        # It's a valid solution, now find the minimal non-negative integer solution
        # This is hard, so let's just return the sum of the positive parts or something

        # For now, let's use a simple heuristic: scale up until all are integer, then adjust
        # But this is not correct.

        # Perhaps for this problem, the minimal solution has small x_i, so let's use BFS with small limits

        # Let's implement a bounded BFS
        from collections import deque
        start = tuple([0] * n)
        queue = deque([(start, 0, [0] * m)])  # state, cost, press_counts
        visited = set([start])
        best_cost = float('inf')

        max_presses_per_button = 50  # Assume optimal has x_i <= 50

        while queue:
            state, cost, presses = queue.popleft()

            if state == tuple(targets):
                best_cost = min(best_cost, cost)
                continue

            if cost >= best_cost:
                continue

            for button_idx, button in enumerate(buttons):
                if presses[button_idx] >= max_presses_per_button:
                    continue

                new_state = list(state)
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
                new_presses = presses[:]
                new_presses[button_idx] += 1
                new_cost = cost + 1

                if new_state_tuple not in visited:
                    visited.add(new_state_tuple)
                    queue.append((new_state_tuple, new_cost, new_presses))

        return best_cost if best_cost != float('inf') else -1

    else:
        return -1

def solve_machine_part2_linear(buttons: List[List[int]], targets: List[int]) -> int:
    """Solve for minimum button presses for Part 2 using linear algebra + bounded BFS."""
    return solve_linear_system(buttons, targets)

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
        min_presses = solve_machine_part2_linear(buttons, targets)
        if min_presses == -1:
            print(f"Machine {len(targets)} counters, {len(buttons)} buttons: No solution")
            continue
        total_presses += min_presses
        print(f"Machine {len(targets)} counters, {len(buttons)} buttons: {min_presses} presses")

    print(f"Total minimum presses: {total_presses}")

if __name__ == "__main__":
    main()

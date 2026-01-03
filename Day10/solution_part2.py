#!/usr/bin/env python3

import sys
from typing import List, Tuple
from collections import deque

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

def solve_machine_part2(buttons: List[List[int]], targets: List[int]) -> int:
    """Solve for minimum button presses for Part 2 using BFS."""
    n = len(targets)  # number of counters
    m = len(buttons)  # number of buttons

    # Start from all zeros
    start_state = tuple([0] * n)
    target_state = tuple(targets)

    # BFS queue: (current_state, presses_used)
    queue = deque([(start_state, 0)])
    visited = set([start_state])

    while queue:
        current_state, presses = queue.popleft()

        if current_state == target_state:
            return presses

        # Try pressing each button
        for button_idx, button in enumerate(buttons):
            new_state = list(current_state)
            valid = True

            # Apply button press
            for counter_idx in button:
                if counter_idx < n:
                    new_state[counter_idx] += 1
                    # Prune if we exceed the target (can't go back)
                    if new_state[counter_idx] > targets[counter_idx]:
                        valid = False
                        break

            if not valid:
                continue

            new_state_tuple = tuple(new_state)
            if new_state_tuple not in visited:
                visited.add(new_state_tuple)
                queue.append((new_state_tuple, presses + 1))

    # If we reach here, no solution found (shouldn't happen for valid problems)
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
        min_presses = solve_machine_part2(buttons, targets)
        total_presses += min_presses
        print(f"Machine {len(targets)} counters, {len(buttons)} buttons: {min_presses} presses")

    print(f"Total minimum presses: {total_presses}")

if __name__ == "__main__":
    main()

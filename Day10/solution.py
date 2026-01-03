#!/usr/bin/env python3

import sys
from typing import List, Tuple
from itertools import product

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

def solve_machine(target: List[int], buttons: List[List[int]]) -> int:
    """Solve for minimum button presses for a single machine using BFS."""
    n = len(target)  # number of lights
    m = len(buttons)  # number of buttons

    # Convert target to tuple for hashing
    target_tuple = tuple(target)

    # BFS queue: (current_state, presses_used)
    from collections import deque
    queue = deque([(tuple([0] * n), 0)])  # Start with all lights off, 0 presses
    visited = set([tuple([0] * n)])

    while queue:
        current_state, presses = queue.popleft()

        if current_state == target_tuple:
            return presses

        # Try pressing each button
        for button_idx, button in enumerate(buttons):
            new_state = list(current_state)
            # Toggle the lights affected by this button
            for light_idx in button:
                if light_idx < n:  # Ensure index is valid
                    new_state[light_idx] ^= 1

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

        target, buttons = parse_machine(line)
        min_presses = solve_machine(target, buttons)
        total_presses += min_presses
        print(f"Machine {len(target)} lights, {len(buttons)} buttons: {min_presses} presses")

    print(f"Total minimum presses: {total_presses}")

if __name__ == "__main__":
    main()

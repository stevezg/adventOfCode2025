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

def solve_machine_part2_bounded(buttons: List[List[int]], targets: List[int], max_presses_per_button: int = 300) -> int:
    """Solve for minimum button presses for Part 2 using bounded BFS."""
    n = len(targets)  # number of counters
    m = len(buttons)  # number of buttons

    # Start from all zeros
    start_state = tuple([0] * n)
    target_state = tuple(targets)

    # BFS queue: (current_state, presses_used, press_counts)
    queue = deque([(start_state, 0, [0] * m)])
    visited = set([start_state])
    best_cost = float('inf')

    while queue:
        current_state, presses, press_counts = queue.popleft()

        if current_state == target_state:
            best_cost = min(best_cost, presses)
            continue

        if presses >= best_cost:
            continue

        # Try pressing each button
        for button_idx, button in enumerate(buttons):
            if press_counts[button_idx] >= max_presses_per_button:
                continue

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
            new_press_counts = press_counts[:]
            new_press_counts[button_idx] += 1

            if new_state_tuple not in visited:
                visited.add(new_state_tuple)
                queue.append((new_state_tuple, presses + 1, new_press_counts))

    return best_cost if best_cost != float('inf') else -1

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
        min_presses = solve_machine_part2_bounded(buttons, targets)
        if min_presses == -1:
            print(f"Machine {len(targets)} counters, {len(buttons)} buttons: No solution found (try increasing max_presses_per_button)")
            continue
        total_presses += min_presses
        print(f"Machine {len(targets)} counters, {len(buttons)} buttons: {min_presses} presses")

    print(f"Total minimum presses: {total_presses}")

if __name__ == "__main__":
    main()

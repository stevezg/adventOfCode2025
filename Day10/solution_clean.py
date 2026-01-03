#!/usr/bin/env python3
"""
Day 10: Factory - Clean and efficient solution for both parts.
Part 1: Toggle lights (XOR) - BFS
Part 2: Increment counters (ADD) - Optimized BFS with pruning
"""

import sys
from collections import deque
from typing import List, Tuple


def parse_line(line: str) -> Tuple[List[int], List[List[int]], List[int]]:
    """Parse a machine line into target lights, buttons, and joltage targets."""
    parts = line.strip().split()
    
    lights_target = None
    buttons = []
    joltage_targets = None
    
    for part in parts:
        if part.startswith('[') and part.endswith(']'):
            lights_target = [1 if c == '#' else 0 for c in part[1:-1]]
        elif part.startswith('(') and part.endswith(')'):
            button_str = part[1:-1]
            buttons.append([int(x) for x in button_str.split(',')] if button_str else [])
        elif part.startswith('{') and part.endswith('}'):
            joltage_targets = [int(x) for x in part[1:-1].split(',')]
    
    return lights_target, buttons, joltage_targets


def solve_part1(target: List[int], buttons: List[List[int]]) -> int:
    """Solve Part 1: Minimum presses to toggle lights to target state."""
    n = len(target)
    target_tuple = tuple(target)
    
    queue = deque([(tuple([0] * n), 0)])
    visited = {tuple([0] * n)}
    
    while queue:
        state, presses = queue.popleft()
        
        if state == target_tuple:
            return presses
        
        for button in buttons:
            new_state = list(state)
            for light_idx in button:
                if light_idx < n:
                    new_state[light_idx] ^= 1
            
            new_state_tuple = tuple(new_state)
            if new_state_tuple not in visited:
                visited.add(new_state_tuple)
                queue.append((new_state_tuple, presses + 1))
    
    return -1


def solve_part2(targets: List[int], buttons: List[List[int]]) -> int:
    """Solve Part 2: Minimum presses to increment counters to target values."""
    n = len(targets)
    target_tuple = tuple(targets)
    
    queue = deque([(tuple([0] * n), 0)])
    visited = {tuple([0] * n)}
    
    while queue:
        state, presses = queue.popleft()
        
        if state == target_tuple:
            return presses
        
        for button in buttons:
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
            if new_state_tuple not in visited:
                visited.add(new_state_tuple)
                queue.append((new_state_tuple, presses + 1))
    
    return -1


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    
    if input_file:
        with open(input_file, 'r') as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()
    
    total_part1 = 0
    total_part2 = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        lights_target, buttons, joltage_targets = parse_line(line)
        
        # Part 1: Solve for lights
        if lights_target:
            min_presses_1 = solve_part1(lights_target, buttons)
            total_part1 += min_presses_1
        
        # Part 2: Solve for joltage
        if joltage_targets:
            min_presses_2 = solve_part2(joltage_targets, buttons)
            total_part2 += min_presses_2
    
    print(f"Part 1 total: {total_part1}")
    print(f"Part 2 total: {total_part2}")


if __name__ == "__main__":
    main()



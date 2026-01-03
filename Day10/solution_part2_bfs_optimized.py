#!/usr/bin/env python3

import sys
from typing import List, Tuple
from collections import deque
import heapq

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

def solve_machine_bfs_optimized(buttons: List[List[int]], targets: List[int]) -> int:
    """Solve using optimized BFS with better pruning.
    
    Key optimizations:
    1. Use tuple for state (immutable, hashable)
    2. Early pruning if state exceeds any target
    3. Only track best distance to each state
    """
    n = len(targets)  # number of counters
    m = len(buttons)  # number of buttons
    
    # Build button effects per counter (for faster lookup)
    button_effects = [set() for _ in range(n)]
    for j, button in enumerate(buttons):
        for i in button:
            if i < n:
                button_effects[i].add(j)
    
    # Check if solution is possible
    for i in range(n):
        if targets[i] > 0 and len(button_effects[i]) == 0:
            return -1  # Counter i needs value but no button affects it
    
    # Start from all zeros
    start_state = tuple([0] * n)
    target_state = tuple(targets)
    
    if start_state == target_state:
        return 0
    
    # BFS with distance tracking
    queue = deque([start_state])
    dist = {start_state: 0}
    
    while queue:
        current_state = queue.popleft()
        current_dist = dist[current_state]
        
        # Try pressing each button
        for j, button in enumerate(buttons):
            new_state_list = list(current_state)
            valid = True
            
            # Apply button press
            for counter_idx in button:
                if counter_idx < n:
                    new_state_list[counter_idx] += 1
                    # Prune if we exceed any target
                    if new_state_list[counter_idx] > targets[counter_idx]:
                        valid = False
                        break
            
            if not valid:
                continue
            
            new_state = tuple(new_state_list)
            
            # Check if we've found the target
            if new_state == target_state:
                return current_dist + 1
            
            # Only add if we haven't seen this state or found a better path
            if new_state not in dist:
                dist[new_state] = current_dist + 1
                queue.append(new_state)
    
    return -1  # No solution found

def solve_machine_astar(buttons: List[List[int]], targets: List[int]) -> int:
    """Solve using A* with heuristic.
    
    Heuristic: max over counters of ceil(remaining[i] / max_buttons_affecting[i])
    """
    n = len(targets)
    m = len(buttons)
    
    # Build button effects per counter
    button_effects = [set() for _ in range(n)]
    max_buttons_per_counter = [0] * n
    for j, button in enumerate(buttons):
        for i in button:
            if i < n:
                button_effects[i].add(j)
                max_buttons_per_counter[i] += 1
    
    def heuristic(state: Tuple[int, ...]) -> int:
        """Estimate remaining presses needed."""
        h = 0
        for i in range(n):
            remaining = targets[i] - state[i]
            if remaining > 0:
                if max_buttons_per_counter[i] == 0:
                    return float('inf')
                # Need at least ceil(remaining / max_buttons_per_counter[i]) presses
                h = max(h, (remaining + max_buttons_per_counter[i] - 1) // max_buttons_per_counter[i])
        return h
    
    start_state = tuple([0] * n)
    target_state = tuple(targets)
    
    if start_state == target_state:
        return 0
    
    # A* priority queue: (f_score, g_score, state)
    # f_score = g_score + heuristic
    g_score = {start_state: 0}
    f_score = {start_state: heuristic(start_state)}
    
    queue = [(f_score[start_state], 0, start_state)]
    heapq.heapify(queue)
    
    while queue:
        current_f, current_g, current_state = heapq.heappop(queue)
        
        # Check if we've already found a better path to this state
        if current_state in g_score and current_g > g_score[current_state]:
            continue
        
        if current_state == target_state:
            return current_g
        
        # Try pressing each button
        for j, button in enumerate(buttons):
            new_state_list = list(current_state)
            valid = True
            
            for counter_idx in button:
                if counter_idx < n:
                    new_state_list[counter_idx] += 1
                    if new_state_list[counter_idx] > targets[counter_idx]:
                        valid = False
                        break
            
            if not valid:
                continue
            
            new_state = tuple(new_state_list)
            tentative_g = current_g + 1
            
            # Only update if this is a better path
            if new_state not in g_score or tentative_g < g_score[new_state]:
                g_score[new_state] = tentative_g
                new_f = tentative_g + heuristic(new_state)
                f_score[new_state] = new_f
                heapq.heappush(queue, (new_f, tentative_g, new_state))
    
    return -1

def solve_machine_part2(buttons: List[List[int]], targets: List[int]) -> int:
    """Main solver - try A* first (usually faster), fallback to BFS."""
    # A* is usually faster for this type of problem
    try:
        result = solve_machine_astar(buttons, targets)
        if result != -1:
            return result
    except:
        pass
    
    # Fallback to BFS
    return solve_machine_bfs_optimized(buttons, targets)

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
            print(f"Machine {line_num}: No solution found", file=sys.stderr)
        else:
            total_presses += min_presses
            if len(lines) <= 10:  # Only print details for small inputs
                print(f"Machine {line_num}: {min_presses} presses")
    
    print(f"Total minimum presses: {total_presses}")

if __name__ == "__main__":
    main()


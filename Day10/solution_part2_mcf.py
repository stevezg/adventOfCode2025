#!/usr/bin/env python3

import sys
from typing import List, Tuple

try:
    from ortools.linear_solver import pywraplp
    HAS_ORTOOLS = True
except ImportError:
    HAS_ORTOOLS = False
    print("Warning: OR-Tools not available, falling back to manual MCF implementation")

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
        return solve_machine_manual_mcf(buttons, targets)

    n = len(targets)  # number of counters
    m = len(buttons)  # number of buttons

    # Create solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        # Fallback to CBC if SCIP is not available
        solver = pywraplp.Solver.CreateSolver('CBC')
        if not solver:
            print("Warning: No ILP solver available, using manual MCF")
            return solve_machine_manual_mcf(buttons, targets)

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

def solve_machine_manual_mcf(buttons: List[List[int]], targets: List[int]) -> int:
    """Solve using manual minimum cost flow (fallback)."""
    from collections import defaultdict
    import heapq

    n = len(targets)  # number of counters
    m = len(buttons)  # number of buttons

    # Total flow needed
    total_flow = sum(targets)

    # Build the graph
    # Nodes: 0 to m-1: buttons, m to m+n-1: counters
    graph = defaultdict(list)

    # Edges from buttons to counters they affect
    for button_idx, button in enumerate(buttons):
        for counter_idx in button:
            if counter_idx < n:
                # Edge: button -> counter, cost=1, capacity=infinity
                graph[button_idx].append((m + counter_idx, 1, float('inf')))
                graph[m + counter_idx].append((button_idx, -1, 0))  # reverse edge

    # Now use successive shortest path to send flow
    total_cost = 0
    remaining_demand = targets[:]

    while sum(remaining_demand) > 0:
        # Find shortest path from any button to any counter with remaining demand
        # Use Dijkstra to find minimum cost path

        # Distances and previous nodes
        dist = {}
        prev = {}
        pq = []

        # Start from all buttons
        for button_idx in range(m):
            dist[button_idx] = 0
            prev[button_idx] = None
            heapq.heappush(pq, (0, button_idx))

        # Also add counters with demand as potential targets
        for counter_idx in range(n):
            if remaining_demand[counter_idx] > 0:
                dist[m + counter_idx] = float('inf')

        while pq:
            cost, node = heapq.heappop(pq)

            if cost > dist.get(node, float('inf')):
                continue

            for neighbor, edge_cost, capacity in graph[node]:
                if capacity > 0:  # only consider edges with capacity
                    new_cost = cost + edge_cost
                    if new_cost < dist.get(neighbor, float('inf')):
                        dist[neighbor] = new_cost
                        prev[neighbor] = node
                        heapq.heappush(pq, (new_cost, neighbor))

        # Find the minimum cost among reachable counters with demand
        min_cost_to_sink = float('inf')
        best_sink = None
        for counter_idx in range(n):
            if remaining_demand[counter_idx] > 0 and m + counter_idx in dist:
                if dist[m + counter_idx] < min_cost_to_sink:
                    min_cost_to_sink = dist[m + counter_idx]
                    best_sink = m + counter_idx

        if best_sink is None:
            # No path found
            return -1

        # Send one unit of flow along the path
        total_cost += min_cost_to_sink

        # Update demands
        remaining_demand[best_sink - m] -= 1

    return total_cost

def solve_machine_part2_mcf(buttons: List[List[int]], targets: List[int]) -> int:
    """Solve for minimum button presses for Part 2 using ILP (or MCF fallback)."""
    return solve_machine_ilp(buttons, targets)

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
        min_presses = solve_machine_part2_mcf(buttons, targets)
        total_presses += min_presses
        print(f"Machine {len(targets)} counters, {len(buttons)} buttons: {min_presses} presses")

    print(f"Total minimum presses: {total_presses}")

if __name__ == "__main__":
    main()

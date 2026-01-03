import os
from collections import defaultdict, deque

def read_input(filename="input.md"):
    """Reads the puzzle input and builds the graph of devices."""
    if not os.path.exists(filename):
        print(f"Error: Input file '{filename}' not found.")
        return None
    
    graph = defaultdict(list)
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Parse format: "device: output1 output2 ..."
            if ':' not in line:
                continue
                
            parts = line.split(':', 1)
            device = parts[0].strip()
            outputs = parts[1].strip().split()
            
            graph[device] = outputs
    
    return graph

def find_reachable_nodes(graph, start):
    """Find all nodes reachable from start using BFS."""
    reachable = set()
    queue = deque([start])
    reachable.add(start)
    
    while queue:
        node = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor not in reachable:
                reachable.add(neighbor)
                queue.append(neighbor)
    
    return reachable

def find_nodes_reaching_target(graph, target):
    """Find all nodes that can reach target by building reverse graph."""
    reverse_graph = defaultdict(list)
    
    for node, outputs in graph.items():
        for output in outputs:
            reverse_graph[output].append(node)
    
    reachable = set()
    queue = deque([target])
    reachable.add(target)
    
    while queue:
        node = queue.popleft()
        for neighbor in reverse_graph.get(node, []):
            if neighbor not in reachable:
                reachable.add(neighbor)
                queue.append(neighbor)
    
    return reachable

def count_paths_between(graph, start, end):
    """Count all paths from start to end (simple case, no constraints)."""
    from_start = find_reachable_nodes(graph, start)
    to_end = find_nodes_reaching_target(graph, end)
    relevant = from_start & to_end
    
    if start not in relevant or end not in relevant:
        return 0
    
    pruned_graph = {}
    for node in relevant:
        pruned_graph[node] = [n for n in graph.get(node, []) if n in relevant]
    
    dp = defaultdict(int)
    dp[end] = 1
    
    changed = True
    iterations = 0
    max_iterations = len(relevant)
    
    while changed and iterations < max_iterations:
        changed = False
        iterations += 1
        
        for node in relevant:
            if node == end:
                continue
            
            total = 0
            for child in pruned_graph.get(node, []):
                total += dp.get(child, 0)
            
            old_val = dp.get(node, 0)
            if total != old_val:
                dp[node] = total
                changed = True
    
    return dp.get(start, 0)

def count_paths_with_constraints(graph, start, end, required_nodes):
    """
    Count all paths from start to end that visit all required nodes (in any order).
    
    Strategy: Split the path into segments:
    1. Count paths visiting node1 then node2: start -> ... -> node1 -> ... -> node2 -> ... -> end
    2. Count paths visiting node2 then node1: start -> ... -> node2 -> ... -> node1 -> ... -> end
    3. Sum them
    
    For each ordering, we use: paths(start->node1) * paths(node1->node2) * paths(node2->end)
    """
    if len(required_nodes) != 2:
        raise ValueError(f"Currently only supports 2 required nodes, got {len(required_nodes)}")
    
    node1, node2 = required_nodes
    
    # Check that all nodes are reachable
    from_start = find_reachable_nodes(graph, start)
    to_end = find_nodes_reaching_target(graph, end)
    
    if start not in from_start or end not in to_end:
        return 0
    if node1 not in from_start or node2 not in from_start:
        return 0
    if node1 not in to_end or node2 not in to_end:
        return 0
    
    # Count paths with node1 before node2
    paths1_to_2 = count_paths_between(graph, node1, node2)
    if paths1_to_2 > 0:
        paths_start_to_1 = count_paths_between(graph, start, node1)
        paths_2_to_end = count_paths_between(graph, node2, end)
        count1 = paths_start_to_1 * paths1_to_2 * paths_2_to_end
    else:
        count1 = 0
    
    # Count paths with node2 before node1
    paths2_to_1 = count_paths_between(graph, node2, node1)
    if paths2_to_1 > 0:
        paths_start_to_2 = count_paths_between(graph, start, node2)
        paths_1_to_end = count_paths_between(graph, node1, end)
        count2 = paths_start_to_2 * paths2_to_1 * paths_1_to_end
    else:
        count2 = 0
    
    return count1 + count2

def solve():
    """Main solve function for Part 2."""
    graph = read_input("input.md")
    
    if graph is None:
        return
    
    # Count paths from "svr" to "out" that visit both "dac" and "fft"
    num_paths = count_paths_with_constraints(graph, "svr", "out", ["dac", "fft"])
    
    print(f"Number of paths from 'svr' to 'out' visiting both 'dac' and 'fft': {num_paths}")

if __name__ == "__main__":
    solve()

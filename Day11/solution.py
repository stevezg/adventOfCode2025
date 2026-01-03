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
    # Build reverse graph (incoming edges)
    reverse_graph = defaultdict(list)
    
    for node, outputs in graph.items():
        for output in outputs:
            reverse_graph[output].append(node)
    
    # BFS from target backwards
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

def count_paths_iterative(graph, start, end):
    """
    Count all paths from start to end using iterative DP with topological ordering.
    
    For counting paths TO end, we process nodes in reverse topological order:
    nodes closer to end (with no paths to other nodes in the subgraph) first.
    
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    # Prune unreachable nodes to reduce graph size
    from_start = find_reachable_nodes(graph, start)
    to_end = find_nodes_reaching_target(graph, end)
    relevant = from_start & to_end
    
    if start not in relevant or end not in relevant:
        return 0
    
    # Build pruned graph with only relevant nodes
    pruned_graph = {}
    for node in relevant:
        pruned_graph[node] = [n for n in graph.get(node, []) if n in relevant]
    
    # Use iterative approach: process nodes multiple times until convergence
    # This is simpler and works correctly for DAGs
    dp = defaultdict(int)
    dp[end] = 1
    
    # Process until no more updates (convergence)
    changed = True
    iterations = 0
    max_iterations = len(relevant)  # Safety limit
    
    while changed and iterations < max_iterations:
        changed = False
        iterations += 1
        
        # Process each node: paths from node = sum of paths from its children
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

def count_paths(graph, start, end):
    """
    Count all paths from start to end using iterative approach.
    This avoids recursion depth issues and uses less memory.
    """
    return count_paths_iterative(graph, start, end)

def solve():
    """Main solve function."""
    graph = read_input("input.md")
    
    if graph is None:
        return
    
    # Count paths from "you" to "out"
    num_paths = count_paths(graph, "you", "out")
    
    print(f"Number of paths from 'you' to 'out': {num_paths}")

if __name__ == "__main__":
    solve()
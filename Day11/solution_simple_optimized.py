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

def prune_unreachable_nodes(graph, start, end):
    """
    Prune nodes that aren't on any path from start to end.
    This can significantly reduce graph size if there are many isolated nodes.
    """
    # Find nodes reachable from start
    from_start = set()
    queue = deque([start])
    from_start.add(start)
    
    while queue:
        node = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor not in from_start:
                from_start.add(neighbor)
                queue.append(neighbor)
    
    # Build reverse graph to find nodes that can reach end
    reverse_graph = defaultdict(list)
    for node, outputs in graph.items():
        for output in outputs:
            reverse_graph[output].append(node)
    
    to_end = set()
    queue = deque([end])
    to_end.add(end)
    
    while queue:
        node = queue.popleft()
        for neighbor in reverse_graph.get(node, []):
            if neighbor not in to_end:
                to_end.add(neighbor)
                queue.append(neighbor)
    
    # Keep only nodes that are both reachable from start AND can reach end
    relevant = from_start & to_end
    
    if start not in relevant or end not in relevant:
        return {}
    
    # Build pruned graph
    pruned = {}
    for node in relevant:
        if node in graph:
            pruned[node] = [n for n in graph[node] if n in relevant]
        else:
            pruned[node] = []
    
    return pruned

def count_paths(graph, start, end, memo=None):
    """
    Count all paths from start to end using dynamic programming with memoization.
    
    Time Complexity: O(V + E) where V = vertices, E = edges
    Space Complexity: O(V) for memoization
    
    Args:
        graph: Dictionary mapping devices to their outputs
        start: Starting device
        end: Ending device
        memo: Memoization dictionary
    
    Returns:
        Number of paths from start to end
    """
    if memo is None:
        memo = {}
    
    # Base case: if we've reached the end, count this as one path
    if start == end:
        return 1
    
    # If we've already computed this, return the cached result
    if start in memo:
        return memo[start]
    
    # If the device has no outputs, there are no paths
    if start not in graph or not graph[start]:
        memo[start] = 0
        return 0
    
    # Recursively count paths through each output
    total_paths = 0
    for output in graph[start]:
        total_paths += count_paths(graph, output, end, memo)
    
    memo[start] = total_paths
    return total_paths

def solve():
    """Main solve function."""
    graph = read_input("input.md")
    
    if graph is None:
        return
    
    # Optional: Prune unreachable nodes (may speed up if graph has many isolated nodes)
    pruned_graph = prune_unreachable_nodes(graph, "you", "out")
    if pruned_graph:
        graph = pruned_graph
    
    # Count paths from "you" to "out"
    num_paths = count_paths(graph, "you", "out")
    
    print(f"Number of paths from 'you' to 'out': {num_paths}")

if __name__ == "__main__":
    solve()



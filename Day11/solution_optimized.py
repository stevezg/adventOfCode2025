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
    all_nodes = set()
    
    for node, outputs in graph.items():
        all_nodes.add(node)
        for output in outputs:
            reverse_graph[output].append(node)
            all_nodes.add(output)
    
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

def topological_sort(graph, start, end):
    """
    Perform topological sort of nodes reachable from start that can reach end.
    Returns list of nodes in reverse topological order.
    """
    # Find relevant nodes
    from_start = find_reachable_nodes(graph, start)
    to_end = find_nodes_reaching_target(graph, end)
    relevant = from_start & to_end
    
    if start not in relevant or end not in relevant:
        return []
    
    # Build graph with only relevant nodes
    filtered_graph = {node: [n for n in outputs if n in relevant] 
                     for node, outputs in graph.items() if node in relevant}
    
    # Calculate in-degrees
    in_degree = defaultdict(int)
    for node in relevant:
        in_degree[node] = 0
    
    for node, outputs in filtered_graph.items():
        for output in outputs:
            in_degree[output] += 1
    
    # Kahn's algorithm for topological sort
    queue = deque([node for node in relevant if in_degree[node] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in filtered_graph.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Reverse to get nodes in order from end to start
    result.reverse()
    return result

def count_paths_iterative(graph, start, end):
    """
    Count all paths from start to end using iterative bottom-up DP.
    More cache-friendly than recursive approach.
    """
    # Get topologically sorted nodes (in reverse order: end first, start last)
    topo_order = topological_sort(graph, start, end)
    
    if not topo_order or start not in topo_order or end not in topo_order:
        return 0
    
    # DP: dp[node] = number of paths from node to end
    dp = defaultdict(int)
    dp[end] = 1
    
    # Process nodes in reverse topological order
    # (from end towards start, so dependencies are resolved first)
    for node in topo_order:
        if node == end:
            continue
        
        # Sum paths through all outputs
        for output in graph.get(node, []):
            if output in dp:
                dp[node] += dp[output]
    
    return dp[start]

def count_paths_recursive(graph, start, end, memo=None):
    """
    Original recursive approach with memoization.
    O(V + E) time, O(V) space.
    """
    if memo is None:
        memo = {}
    
    if start == end:
        return 1
    
    if start in memo:
        return memo[start]
    
    if start not in graph or not graph[start]:
        memo[start] = 0
        return 0
    
    total_paths = 0
    for output in graph[start]:
        total_paths += count_paths_recursive(graph, output, end, memo)
    
    memo[start] = total_paths
    return total_paths

def solve():
    """Main solve function."""
    graph = read_input("input.md")
    
    if graph is None:
        return
    
    # Count paths from "you" to "out" using optimized iterative approach
    num_paths = count_paths_iterative(graph, "you", "out")
    
    print(f"Number of paths from 'you' to 'out': {num_paths}")

if __name__ == "__main__":
    solve()

import math
from collections import defaultdict
from typing import List, Tuple, Set

def read_input(filename: str) -> List[Tuple[int, int, int]]:
    """Read 3D coordinates from input file."""
    points = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                x, y, z = map(int, line.strip().split(','))
                points.append((x, y, z))
    return points

def euclidean_distance(p1: Tuple[int, int, int], p2: Tuple[int, int, int]) -> float:
    """Calculate Euclidean distance between two 3D points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

def compute_all_distances(points: List[Tuple[int, int, int]]) -> List[Tuple[float, int, int]]:
    """
    Compute distances between all pairs of points.

    This is O(n²) time complexity - for each of n points, we compute distance
    to all other points. This creates n*(n-1)/2 unique pairs.

    Returns list of (distance, point1_index, point2_index) tuples.
    """
    distances = []
    n = len(points)

    for i in range(n):
        for j in range(i + 1, n):  # Only compute each pair once
            dist = euclidean_distance(points[i], points[j])
            distances.append((dist, i, j))

    return distances

def compute_distances_optimized(points: List[Tuple[int, int, int]], k: int = 1000) -> List[Tuple[float, int, int]]:
    """
    Optimized version using a max-heap to keep only top k distances.

    Instead of storing all n² distances, we maintain a heap of size k.
    This reduces space complexity from O(n²) to O(k) when k << n².

    Time complexity remains O(n² log k) due to heap operations.
    """
    import heapq

    n = len(points)
    max_heap = []  # Python heapq is min-heap, so we use negative distances

    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(points[i], points[j])

            if len(max_heap) < k:
                heapq.heappush(max_heap, (-dist, i, j))
            elif -dist > max_heap[0][0]:  # Current distance is smaller than largest in heap
                heapq.heapreplace(max_heap, (-dist, i, j))

    # Convert back to min-heap format (positive distances)
    return [(-dist, i, j) for dist, i, j in max_heap]

def find_connected_components(graph: List[List[int]]) -> List[List[int]]:
    """
    Find all connected components in an undirected graph using DFS.

    Args:
        graph: Adjacency list representation

    Returns:
        List of components, where each component is a list of node indices
    """
    n = len(graph)
    visited = [False] * n
    components = []

    def dfs(node: int, component: List[int]):
        """Depth-first search to find all nodes in a component."""
        visited[node] = True
        component.append(node)

        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor, component)

    for i in range(n):
        if not visited[i]:
            component = []
            dfs(i, component)
            components.append(component)

    return components

class UnionFind:
    """Disjoint Set Union (Union-Find) data structure for cycle detection in Kruskal's algorithm."""

    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x: int) -> int:
        """Find the root parent of x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Union two sets. Returns True if union was successful (no cycle),
        False if they were already in the same set (would create cycle).
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # Already in same component

        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True

def kruskal_mst(points: List[Tuple[int, int, int]]) -> Tuple[float, int, int]:
    """
    Kruskal's algorithm to find the MST and return the last edge added.

    Returns (distance, point1_index, point2_index) of the final connecting edge.
    """
    n = len(points)
    uf = UnionFind(n)

    # Generate all possible edges
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(points[i], points[j])
            edges.append((dist, i, j))

    # Sort edges by distance (Kruskal's algorithm)
    edges.sort()

    # Add edges until we have only 1 component
    components = n
    last_edge = None

    for dist, i, j in edges:
        if uf.union(i, j):  # Successfully added edge
            components -= 1
            last_edge = (dist, i, j)

            # If we have only 1 component left, this was the last edge
            if components == 1:
                break

    return last_edge

def solve_part2(input_file: str) -> int:
    """
    Part 2: Find the last edge that connects all junction boxes into one circuit.

    Uses Kruskal's MST algorithm to find the edge that connects the final two components,
    then multiplies the X coordinates of those two points.
    """
    points = read_input(input_file)
    n = len(points)
    print(f"Part 2: Read {n} junction boxes")

    print("Building MST using Kruskal's algorithm...")
    last_edge = kruskal_mst(points)

    if last_edge is None:
        return 0  # Should not happen

    dist, i, j = last_edge
    x1, y1, z1 = points[i]
    x2, y2, z2 = points[j]

    result = x1 * x2
    print(f"Last connecting edge: Point {i} ({x1},{y1},{z1}) ↔ Point {j} ({x2},{y2},{z2})")
    print(f"Distance: {dist:.2f}")
    print(f"X coordinate product: {x1} × {x2} = {result}")

    return result

def solve_brute_force(input_file: str) -> int:
    """
    Brute force solution to Day 8.

    Algorithm steps:
    1. Read all junction box coordinates
    2. Compute distances between all pairs (O(n²))
    3. Sort pairs by distance and take first 1000
    4. Build graph with these edges
    5. Find connected components
    6. Multiply sizes of three largest components
    """
    # Step 1: Read input
    points = read_input(input_file)
    n = len(points)
    print(f"Read {n} junction boxes")

    # Step 2: Compute all pairwise distances (brute force O(n²))
    print("Computing all pairwise distances...")
    if n <= 100:  # For small n, brute force is fine
        distances = compute_all_distances(points)
        print(f"Computed {len(distances)} unique pairs")
        # Step 3: Sort by distance and take top 1000
        print("Sorting distances and selecting top 1000 pairs...")
        distances.sort()  # Sort by distance (first element of tuple)
        selected_pairs = distances[:min(1000, len(distances))]
    else:  # For larger n, use optimized version
        print("Using optimized distance computation...")
        selected_pairs = compute_distances_optimized(points, 1000)
        print(f"Selected top {len(selected_pairs)} pairs")

    # Step 4: Build graph
    print("Building graph with selected connections...")
    graph = [[] for _ in range(n)]
    for dist, i, j in selected_pairs:
        graph[i].append(j)
        graph[j].append(i)

    # Step 5: Find connected components
    print("Finding connected components...")
    components = find_connected_components(graph)

    # Step 6: Get sizes of three largest components
    component_sizes = sorted([len(comp) for comp in components], reverse=True)
    print(f"Component sizes: {component_sizes[:10]}...")  # Show first 10

    # Multiply three largest
    if len(component_sizes) >= 3:
        result = component_sizes[0] * component_sizes[1] * component_sizes[2]
    else:
        result = 0  # Not enough components

    return result

if __name__ == "__main__":
    # Assuming input.txt exists in the same directory
    try:
        print("=== Day 8 Part 1 ===")
        result1 = solve_brute_force("input.txt")
        print(f"Part 1 Result: {result1}")

        print("\n=== Day 8 Part 2 ===")
        result2 = solve_part2("input.txt")
        print(f"Part 2 Result: {result2}")
    except FileNotFoundError:
        print("Please provide input.txt file with junction box coordinates")

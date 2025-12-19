# Day 7: Tachyon Manifold Walkthrough

## The Problem
We needed to simulate a tachyon beam traveling through a manifold.
- Beams travel **downward**.
- If a beam hits a **splitter** (`^`), it stops, and two new beams appear at the immediate left and right of the splitter in the next step.
- We need to count the total number of splits.

## The Approach
We used a **row-by-row simulation**.

1.  **Parse the Grid**: Read the input into a 2D grid.
2.  **Find the Start**: Locate the 'S' character in the first row. This is our initial beam.
3.  **Simulate**:
    - We maintain a `set` of active column indices for the current row.
    - We iterate through each row of the grid.
    - For each row, we determine the `next_beams` (columns active in the next row) based on the current row's active columns and the grid contents.
    - If a beam hits `^`, we increment the `splits` counter and add `col - 1` and `col + 1` to the `next_beams` set (checking for boundaries).
    - If a beam hits `.`, it continues to `col` in `next_beams`.

## The Code
The core logic in [day7.py](file:///Users/stephenanderson/Documents/Code/Python/Advent-of-Code/Advent-of-code-2025/adventOfCode2025/Day7/day7.py) handles the simulation:

```python
    for r in range(1, rows):
        next_beams = set()
        for c in current_beams:
            if grid[r][c] == '^':
                splits += 1  # Count split
                if c - 1 >= 0: next_beams.add(c - 1)
                if c + 1 < cols: next_beams.add(c + 1)
            elif grid[r][c] == '.':
                next_beams.add(c)
        current_beams = next_beams
```

## Results
- **Example Input**: Result was **21** splits.
- **Your Input**: Result was **1609** splits.

The simulation was efficient enough because the number of columns is small, and we process each row exactly once.

## Tree-Based Alternative
We also implemented a **Tree/Graph Traversal** based solution in [day7_tree.py](file:///Users/stephenanderson/Documents/Code/Python/Advent-of-Code/Advent-of-code-2025/adventOfCode2025/Day7/day7_tree.py).
- This approach treats the splitters as nodes in a graph.
- We perform a traversal (like BFS) starting from 'S' to find all reachable splitters.
- This confirms the result of **1609** splitters.

## Performance Comparison
Both solutions handle the input almost instantly, but the **Tree-Based** approach was slightly faster in our test:
- **Row-by-Row**: ~0.05s
- **Tree-Based**: ~0.02s

The Tree approach prunes redundant paths more naturally by tracking `visited_state`, whereas the row-by-row explicitly processes every active beam at every row step, involving more set allocations.

## Complexity Analysis
Let $N$ be the total number of cells in the grid ($Rows \times Cols$).

### Row-by-Row Solution
- **Runtime**: $O(N)$ in the worst case.
  - We verify each active beam at each row. in the worst case (full flood), we check $Cols$ beams for $Rows$ rows.
  - However, for sparse beams, it runs closer to $O(L)$ where $L$ is the total length of all beam paths combined.
- **Space**: $O(Cols)$ to store the set of active beam columns for the current row.

### Tree-Based Solution
- **Runtime**: $O(N)$ in the worst case.
  - We visit each reachable cell exactly once due to the `visited` set.
- **Space**: $O(N)$ to store the `visited` set of all reachable coordinates.

Both are linear with respect to the grid size, but the **Row-by-Row** approach is more space-efficient ($O(Cols)$ vs $O(N)$).

## Part 2: Quantum Manifold
For Part 2, we needed to count the total number of distinct timelines (paths) the particle could take. Since the number of paths grows exponentially, a simple simulation is too slow.

We used **Dynamic Programming (Memoization)** to efficiently count paths.
1.  **State**: `(r, c)` representing the particle's position.
2.  **Logic**: The number of paths from `(r, c)` is the sum of paths from its children.
    - If `^`: `paths(r+1, c-1) + paths(r+1, c+1)`
    - If `.`: `paths(r+1, c)`
3.  **Memoization**: We store the result for each `(r, c)` to avoid re-calculating it, ensuring each state is processed only once.

```python
    memo = {}
    def count_paths(r, c):
        if r >= rows or c < 0 or c >= cols: return 1  # Exited
        if (r, c) in memo: return memo[(r, c)]
        
        if grid[r][c] == '^':
            # Splitter: Sum of left and right paths
            res = count_paths(r + 1, c - 1) + count_paths(r + 1, c + 1)
        else:
            # Empty space: Continue down
            res = count_paths(r + 1, c)
            
        memo[(r, c)] = res
        return res
```

- **Example Result**: 40
- **Final Result**: 12,472,142,047,197
- **Complexity**: $O(N)$ time and space.



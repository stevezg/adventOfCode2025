import sys

# Increase recursion depth just in case, though for this grid size it might not be strictly necessary
sys.setrecursionlimit(20000)

def solve(input_file):
    with open(input_file, 'r') as f:
        grid = [line.strip() for line in f]

    rows = len(grid)
    cols = len(grid[0])
    
    # Find S
    start_col = -1
    for c in range(cols):
        if grid[0][c] == 'S':
            start_col = c
            break
            
    if start_col == -1:
        print("Start 'S' not found")
        return

    memo = {}

    def count_paths(r, c):
        # Base case: Particle exits manifold (goes below last row)
        if r >= rows:
            return 1
        
        # Boundary check: if c is out of bounds, it also counts as exiting?
        # "exit the manifold"
        # The example text says: "This process continues until all of the tachyon beams reach a splitter or exit the manifold"
        # Since the diagram has width, exiting left/right might be possible too?
        # "Tachyon beams pass freely through empty space (.)"
        # If I am at column -1 or cols, I have exited.
        if c < 0 or c >= cols:
            return 1

        if (r, c) in memo:
            return memo[(r, c)]
        
        cell = grid[r][c]
        
        result = 0
        if cell == '^':
            # Splitter: Left and Right paths
            # "new tachyon beam continues from the immediate left and from the immediate right of the splitter"
            # It seems they continue DOWN from there?
            # As analyzed before, the next effective position is (r+1, c-1) and (r+1, c+1) if we iterate row by row.
            # But wait, looking closer at the diagram again:
            # .......^....... (row r)
            # ......^.^...... (row r+1)
            # Yes, the children are at row r+1.
            # So we recurse to (r+1, c-1) and (r+1, c+1).
            
            result = count_paths(r + 1, c - 1) + count_paths(r + 1, c + 1)
            
        else:
            # Empty space or S
            # "Tachyon beams pass freely through empty space"
            # Continues straight down
            result = count_paths(r + 1, c)
            
        memo[(r, c)] = result
        return result

    # Start recursion from just below S? Or S itself?
    # S acts like empty space usually.
    # We can start at (0, start_col).
    
    total_timelines = count_paths(0, start_col)
    print(f"Total timelines: {total_timelines}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        solve(sys.argv[1])
    else:
        solve('Day7/input.txt')

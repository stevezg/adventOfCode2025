import collections

def solve():
    with open('Day7/input.txt', 'r') as f:
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

    # Queue of beams: (row, col)
    # Beams are just starting points that travel DOWN.
    # We want to find all UNIQUE splitters hit.
    
    queue = collections.deque()
    queue.append((0, start_col))
    
    visited_splitters = set()
    
    # Since we might have multiple paths to the same point that isn't a splitter,
    # we should also avoid redundant processing of empty space if paths merge?
    # Actually, if two beams merge into empty space, they are identical from there on.
    # So we can track visited state as (r, c) for any cell to prune?
    # The problem says beams "pass freely through empty space".
    # And "if a tachyon beam encounters a splitter... a new tachyon beam continues from the immediate left and right".
    # This implies that from any (r, c), the path is deterministic.
    # So yes, we can track visited (r, c) to avoid re-simulating the same path segment.
    
    visited_state = set()

    while queue:
        r, c = queue.popleft()
        
        # Traverse downwards from (r, c)
        curr_r, curr_c = r, c
        
        while curr_r < rows:
            if (curr_r, curr_c) in visited_state:
                # Already processed this path segment
                break
            visited_state.add((curr_r, curr_c))
            
            cell = grid[curr_r][curr_c]
            
            if cell == '^':
                # Splitter hit!
                visited_splitters.add((curr_r, curr_c))
                
                # Spawn new beams if valid
                # Left
                if curr_c - 1 >= 0:
                    queue.append((curr_r, curr_c - 1)) # Starts at same row, left
                    # Wait, problem says "continues from the immediate left... of the splitter"
                    # Does it continue DOWN immediately?
                    # "continues from the immediate left... of the splitter" implies (r, c-1).
                    # And since loops continue "until all... reach a splitter or exit",
                    # the next step for these new beams is r+1?
                    # In my previous code:
                    # if cell == '^': ... next_beams.add(c-1) ...
                    # This added it to next_beams for the NEXT row (r+1).
                    # So essentially the new beam starts at (r+1, c-1).
                    # Let's re-read carefully: "continues from the immediate left... of the splitter".
                    # Example trace: 
                    # .......S.......
                    # .......|.......
                    # ......|^|......
                    # The splitter is at some row. The new beams appear to be at the same row index visually?
                    # No, looking at example:
                    # .......^.......  <- Row R
                    # ......^.^......  <- Row R+1
                    # The new beams appear at (R+1, C-1) and (R+1, C+1) effectively.
                    # Or do they start at (R, C-1) and then move down?
                    # If they start at (R, C-1), and (R, C-1) is empty, they move to (R+1, C-1).
                    # If (R, C-1) is a splitter, it would split immediately.
                    # My previous simulation added to `next_beams` which processed `grid[r]`.
                    # Actually `next_beams` was for iteration `r+1`.
                    # Let's check `day7.py` logic:
                    # `for r in range(1, rows): ... cell = grid[r][c] ... if cell == '^': ... next_beams.add(c-1)`
                    # This means we processed row `r`, found splitter at `c`.
                    # Then for row `r+1`, we check `c-1`.
                    # So effectively, the new beam starts looking for things at `grid[r+1][c-1]`.
                    # This matches the detailed example where from the splitter row, the next things are on the next row.
                    
                # So in this tree traversal:
                # If we are at (curr_r, curr_c) and it is '^':
                # We stop this beam.
                # We spawn children at (curr_r + 1, curr_c - 1) and (curr_r + 1, curr_c + 1).
                
                if curr_r + 1 < rows:
                    if curr_c - 1 >= 0:
                        queue.append((curr_r + 1, curr_c - 1))
                    if curr_c + 1 < cols:
                        queue.append((curr_r + 1, curr_c + 1))
                break 
            
            # If not splitter, continue down
            curr_r += 1

    print(f"Total unique splitters activated: {len(visited_splitters)}")

if __name__ == '__main__':
    solve()

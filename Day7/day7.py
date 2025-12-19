def solve():
    with open('Day7/input.txt', 'r') as f:
        grid = [line.strip() for line in f]

    rows = len(grid)
    cols = len(grid[0])
    
    # Find S
    beams = set() # Set of column indices
    for c in range(cols):
        if grid[0][c] == 'S':
            beams.add(c)
            break
            
    if not beams:
        print("Start 'S' not found")
        return

    splits = 0
    
    # Simulate row by row, starting from the row after S
    # Initial S row is already processed by finding S
    
    # Actually, we should process the grid flow.
    # The beam starts at S and goes down.
    # For each row, we check the active beams.
    # We iterate rows 1 to end (assuming S is at row 0)
    
    current_beams = beams
    
    # The problem says S is the start. 
    # "incoming tachyon beam extends downward from S"
    # So at row 0, we have a beam at S_col.
    # For each row index r:
    #   We have a set of active beam columns entering this row.
    #   We check grid[r][c] for each active c.
    #   If cell is '.', beam continues to next row same col.
    #   If cell is '^', beam stops. Splits: new beams at c-1 and c+1 for next row.
    #      Also count split.
    #      HOWEVER, "beam is stopped; instead, a new tachyon beam continues from the immediate left and from the immediate right of the splitter."
    #      This happens IN THE SAME ROW potentially? Or standard grid physics?
    #      Looking at the example:
    #      .......S.......
    #      .......|.......
    #      .......^.......
    #      ......^.^......
    #      The split happens AT the splitter.
    #      The new beams start from left and right OF THE SPLITTER.
    #      It seems they continue downward from there.
    #      So if splitter at (r, c), next row active beams include (c-1) and (c+1).
    #      Original beam at c stops (doesn't continue to r+1 at c).
    
    for r in range(1, rows):
        next_beams = set()
        for c in current_beams:
            # Check what is at this cell
            cell = grid[r][c]
            
            if cell == '.':
                # Continues down
                next_beams.add(c)
            elif cell == '^':
                # Splitter
                # 1. Increment split count
                # 2. Add left and right to next_beams IF valid
                # Note: "beam is stopped" means we don't add c to next_beams
                
                splits += 1
                
                if c - 1 >= 0:
                    next_beams.add(c - 1)
                if c + 1 < cols:
                    next_beams.add(c + 1)
            elif cell == 'S':
                 # Should not happen below top row usually, but treat as empty space?
                 # Problem says S is entrance.
                 next_beams.add(c)
            else:
                # Unknown char? Assume empty space or block?
                # Problem says empty space is '.'
                # Lets assume only . S ^ exist based on description
                pass
                
        current_beams = next_beams
        
        # If no beams left, we can stop? Or should we safeguard?
        if not current_beams:
            break
            
    print(f"Total splits: {splits}")

if __name__ == '__main__':
    solve()

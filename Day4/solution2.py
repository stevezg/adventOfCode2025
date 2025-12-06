import os

# Define the 8 possible offsets for adjacent cells
NEIGHBOR_OFFSETS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1), (1, 0),   (1, 1)
]

def read_input(filename="input.md"):
    """Reads the grid input from the file."""
    if not os.path.exists(filename):
        print(f"Error: Input file '{filename}' not found.")
        return []
    with open(filename, 'r') as f:
        # Read all non-empty, stripped lines to form the grid
        return [list(line.strip()) for line in f if line.strip()]

def get_neighbor_roll_count(grid, r, c, H, W):
    """Counts the number of paper rolls (@) adjacent to (r, c)."""
    neighbor_count = 0
    
    for dr, dc in NEIGHBOR_OFFSETS:
        nr, nc = r + dr, c + dc # Neighbor Row, Neighbor Column
        
        # Boundary Check
        if 0 <= nr < H and 0 <= nc < W:
            
            # Roll Check: Only count rolls that are currently present (@)
            if grid[nr][nc] == '@':
                neighbor_count += 1
                
    return neighbor_count

def solve_day4_part2(grid):
    """
    Simulates the iterative removal of paper rolls until no more are accessible.
    """
    if not grid:
        return 0
        
    H = len(grid)
    W = len(grid[0])
    total_removed = 0
    
    # --- Iterative Simulation Loop ---
    while True:
        # List of coordinates (r, c) to be removed in this pass
        removable_list = []
        
        # 1. Find all accessible rolls for this pass
        for r in range(H):
            for c in range(W):
                
                # Check 1: Must be a roll of paper (@)
                if grid[r][c] == '@':
                    
                    # Get count based on the CURRENT state of the grid
                    neighbor_count = get_neighbor_roll_count(grid, r, c, H, W)
                    
                    # Access Check: Accessible if fewer than 4 adjacent rolls
                    if neighbor_count < 4:
                        removable_list.append((r, c))
        
        removals_in_pass = len(removable_list)
        
        # 2. Termination Check
        if removals_in_pass == 0:
            break
            
        # 3. Update Grid and Total Count
        for r, c in removable_list:
            # Change the roll to a '.' (empty space)
            grid[r][c] = '.' 
            
        total_removed += removals_in_pass
        # print(f"Removed {removals_in_pass} rolls in this pass. Total: {total_removed}") # Debugging
        
    return total_removed

# --- Execution Block ---

if __name__ == "__main__":
    
    # Read the grid input
    puzzle_input_grid = read_input()
    
    if not puzzle_input_grid:
        exit() 
    
    # Run the solver
    result = solve_day4_part2(puzzle_input_grid)
    
    print("\n" + "="*50)
    print("🎄 Advent of Code - Day 4, Part 2")
    print("="*50)
    print(f"Total Rolls Removed: {result}")
    print("="*50 + "\n")
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

def solve_day4_part1(grid):
    """
    Counts the number of accessible paper rolls based on the rule: 
    Fewer than four adjacent rolls (@).
    """
    if not grid:
        return 0
        
    H = len(grid)    # Height (number of rows)
    W = len(grid[0]) # Width (number of columns)
    total_accessible_rolls = 0

    # 1. Iterate through every cell in the grid
    for r in range(H):
        for c in range(W):
            
            # Check 1: Must be a roll of paper (@)
            if grid[r][c] == '@':
                
                neighbor_count = 0
                
                # 2. Iterate through the 8 neighbors
                for dr, dc in NEIGHBOR_OFFSETS:
                    nr, nc = r + dr, c + dc # Neighbor Row, Neighbor Column
                    
                    # 3. Boundary Check: Ensure the neighbor is within the grid bounds
                    if 0 <= nr < H and 0 <= nc < W:
                        
                        # 4. Roll Check: Count if the neighbor is also a roll of paper
                        if grid[nr][nc] == '@':
                            neighbor_count += 1
                            
                # 5. Access Check: Accessible if fewer than 4 adjacent rolls
                if neighbor_count < 4:
                    total_accessible_rolls += 1
                    
    return total_accessible_rolls

# --- Execution Block ---

if __name__ == "__main__":
    
    puzzle_input_grid = read_input()
    
    if not puzzle_input_grid:
        exit() 
    
    # Run the solver
    result = solve_day4_part1(puzzle_input_grid)
    
    print("\n" + "="*50)
    print("🎄 Advent of Code - Day 4, Part 1")
    print("="*50)
    print(f"Total Accessible Rolls: {result}")
    print("="*50 + "\n")
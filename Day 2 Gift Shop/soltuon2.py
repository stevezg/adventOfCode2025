import os

# --- Helper Functions ---

def read_input(filename="input.md"):
    """Reads the puzzle input from the specified file."""
    if not os.path.exists(filename):
        print(f"Error: Input file '{filename}' not found.")
        print("Please ensure your puzzle input is saved in that file.")
        return None
    with open(filename, 'r') as f:
        # The input is a single long line, so we read the whole thing and strip whitespace
        return f.read().strip()

def generate_part2_candidates():
    """
    Generates all invalid IDs N formed by repeating a block X at least twice (R >= 2).
    Since the maximum ID size is 10 digits, we check L*R <= 10.
    Returns a set of these invalid IDs.
    """
    candidates = set()
    MAX_DIGITS = 10 
    
    # L is the length of the repeating block X (must be >= 1)
    for L in range(1, MAX_DIGITS + 1):
        
        # R is the number of repetitions (must be >= 2)
        for R in range(2, MAX_DIGITS + 1):
            
            # The total length must not exceed MAX_DIGITS
            total_digits = L * R
            if total_digits > MAX_DIGITS:
                break # Move to the next block length L
            
            # Determine the range for the block X:
            start_block = 10**(L - 1)
            end_block = 10**L
            
            for block_X in range(start_block, end_block):
                # Construct the ID string by repeating the block R times
                s_block = str(block_X)
                s_N = s_block * R 
                N = int(s_N)
                
                # Check for the implicit rule: "None of the numbers have leading zeroes"
                # Since we start 'block_X' at 10**(L-1) (e.g., 10, 100), 
                # the string 's_N' will never have a leading zero, so this is safe.
                
                candidates.add(N)
                
    return candidates

# --- Part 2 Solver Function ---

def solve_day2_part2(input_data):
    """
    Parses the ID ranges and calculates the sum of all invalid IDs 
    (sequence repeated R >= 2 times) that fall within those ranges.
    """
    if not input_data:
        return 0
        
    # 1. Pre-generate the complete set of Part 2 invalid IDs
    all_candidates = generate_part2_candidates()
    
    ranges = input_data.split(',')
    total_sum = 0
    
    # 2. Check the candidates against the large input ranges (O(N_ranges))
    for r in ranges:
        if not r: continue
        try:
            # Parse the "Start-End" range
            start, end = map(int, r.split('-'))
        except ValueError:
            continue

        for candidate in all_candidates:
            if start <= candidate <= end:
                total_sum += candidate
                
    return total_sum

# --- Execution Block ---

if __name__ == "__main__":
    # 1. Read the raw data from input.md
    puzzle_input = read_input()
    
    if puzzle_input is None:
        exit() # Exit if file reading failed
    
    # 2. Run the Part 2 solver function
    result2 = solve_day2_part2(puzzle_input)
    
    # 3. Print the final answer
    print("\n" + "="*40)
    print("🎄 Advent of Code - Day 2, Part 2")
    print("="*40)
    print(f"Part 2 Answer (Sum of Repeated Sequence IDs): {result2}")
    print("="*40 + "\n")
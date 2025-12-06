import os

# --- Input Reader ---

def read_input(filename="input.md"):
    """Reads all lines from the input file."""
    if not os.path.exists(filename):
        print(f"Error: Input file '{filename}' not found.")
        return []
    with open(filename, 'r') as f:
        # Read all non-empty, stripped lines (each is a battery bank)
        return [line.strip() for line in f if line.strip()]

# ----------------------------------------------------
# PART 2: GREEDY OPTIMIZED SOLUTION (O(N*L))
# ----------------------------------------------------

def greedy_solve_part2(bank_string, target_length=12):
    """
    Finds the largest possible subsequence of a fixed length (12) 
    using a monotonic stack (Greedy Algorithm).
    """
    L = len(bank_string)
    
    # Calculate how many digits we must drop
    k_to_drop = L - target_length
    
    # If the bank is too short, we cannot solve it (shouldn't happen in AoC input)
    if k_to_drop < 0:
        return 0 
    
    # Result list acts as a stack to build the optimal sequence
    result = [] 
    
    for digit in bank_string:
        # 1. Discard smaller digits that precede the current larger digit (Greedy choice)
        # While we have digits left to drop AND the current digit is better than the last chosen one
        while result and digit > result[-1] and k_to_drop > 0:
            result.pop()
            k_to_drop -= 1
            
        # 2. Add the current digit
        result.append(digit)
        
    # 3. Handle leftover drops (if the remaining result is longer than 12, 
    # it means the best digits were at the start, and we must drop the smallest ones at the end)
    final_sequence = "".join(result[:target_length])
    
    # Convert the 12-digit string to an integer
    return int(final_sequence)

def part2_optimized(input_data):
    """Calculates the total output joltage for Part 2."""
    total_joltage = 0
    
    # Summing potentially very large numbers requires Python's native handling
    for bank in input_data:
        max_bank_joltage = greedy_solve_part2(bank, target_length=12)
        total_joltage += max_bank_joltage
        
    return total_joltage

# --- Execution Block ---

if __name__ == "__main__":
    
    puzzle_input = read_input()
    
    if not puzzle_input:
        exit() 
    
    # Run the Part 2 solver
    result2 = part2_optimized(puzzle_input)
    
    print("\n" + "="*50)
    print("🎄 Advent of Code - Day 3, Part 2")
    print("="*50)
    print(f"Total Output Joltage (Greedy O(N*L)): {result2}")
    print("="*50 + "\n")
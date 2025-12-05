import os
import time

# --- Input Reader ---

def read_input(filename="input.md"):
    if not os.path.exists(filename):
        print(f"Error: Input file '{filename}' not found.")
        return []
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

# ----------------------------------------------------
# 1. BRUTE-FORCE SOLUTION (O(N*L²))
# ----------------------------------------------------

def brute_force_solve(bank_string):
    n = len(bank_string)
    max_joltage = 0
    for i in range(n):
        tens_digit = int(bank_string[i])
        for j in range(i + 1, n):
            units_digit = int(bank_string[j])
            joltage = tens_digit * 10 + units_digit
            if joltage > max_joltage:
                max_joltage = joltage
    return max_joltage

def part1_brute_force(input_data):
    total_joltage = 0
    start_time = time.perf_counter()
    for bank in input_data:
        total_joltage += brute_force_solve(bank)
    end_time = time.perf_counter()
    return total_joltage, (end_time - start_time)

# ----------------------------------------------------
# 2. OPTIMIZED SOLUTION (O(N*L)) - FIXED
# ----------------------------------------------------

def optimized_solve(bank_string):
    max_joltage = 0
    
    # Initialize to -1 to represent "no digits seen yet".
    # This prevents the last digit of the string from pairing with a "ghost" 0.
    max_unit_digit = -1 
    
    # Iterate backwards
    for i in range(len(bank_string) - 1, -1, -1):
        current_digit = int(bank_string[i])
        
        # 1. ONLY calculate potential joltage if we have a valid unit digit to the right.
        if max_unit_digit != -1:
            potential_joltage = current_digit * 10 + max_unit_digit
            if potential_joltage > max_joltage:
                max_joltage = potential_joltage
        
        # 2. Update the history for the NEXT iteration (to the left).
        # We want the largest digit seen so far.
        if current_digit > max_unit_digit:
            max_unit_digit = current_digit
            
        if max_joltage == 99:
            return 99
            
    return max_joltage

def part1_optimized(input_data):
    total_joltage = 0
    start_time = time.perf_counter()
    for bank in input_data:
        total_joltage += optimized_solve(bank)
    end_time = time.perf_counter()
    return total_joltage, (end_time - start_time)

# ----------------------------------------------------
# 3. EXECUTION BLOCK
# ----------------------------------------------------

if __name__ == "__main__":
    puzzle_input = read_input()
    
    if not puzzle_input:
        exit() 
    
    result_bf, time_bf = part1_brute_force(puzzle_input)
    result_opt, time_opt = part1_optimized(puzzle_input)
    
    print("\n" + "="*50)
    print("🎄 Advent of Code - Day 3, Part 1 Results")
    print("="*50)
    
    print(f"Brute Force Result: {result_bf}")
    print(f"Optimized Result:   {result_opt}")
    
    print("\n--- Runtime Comparison ---")
    print(f"Brute Force Time: {time_bf:.6f} seconds")
    print(f"Optimized Time:   {time_opt:.6f} seconds")
    
    if result_bf == result_opt:
        print("\n✅ Verification Successful: Both methods agree!")
    else:
        print("\n⚠️ ERROR: Logic still differs.")
        
    print("="*50 + "\n")
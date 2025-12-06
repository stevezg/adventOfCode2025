import os
import time

# --- Input Reading and Parsing ---

def read_and_parse_input(filename="input.md"):
    """Reads the input and separates fresh ID ranges from available IDs."""
    if not os.path.exists(filename):
        print(f"Error: Input file '{filename}' not found.")
        return [], []
        
    with open(filename, 'r') as f:
        data = [line.strip() for line in f]

    # Find the blank line separating the two sections
    try:
        separator_index = data.index('')
    except ValueError:
        print("Error: Input file must contain a blank line separating ranges and IDs.")
        return [], []

    range_lines = data[:separator_index]
    id_lines = data[separator_index + 1:]

    # Parse Fresh ID Ranges (A-B)
    fresh_ranges = []
    for line in range_lines:
        if '-' in line:
            try:
                start, end = map(int, line.split('-'))
                fresh_ranges.append((start, end))
            except ValueError:
                continue

    # Parse Available Ingredient IDs
    available_ids = []
    for line in id_lines:
        try:
            available_ids.append(int(line))
        except ValueError:
            continue

    return fresh_ranges, available_ids

# ----------------------------------------------------------------------
# STRATEGY 1: O(N_Ranges * N_IDs) Brute Force (Simple Verification)
# ----------------------------------------------------------------------

def solve_brute_force(fresh_ranges, available_ids):
    """Checks every ID against every range."""
    fresh_count = 0
    
    for id_val in available_ids:
        is_fresh = False
        for start, end in fresh_ranges:
            if start <= id_val <= end:
                is_fresh = True
                break
        if is_fresh:
            fresh_count += 1
            
    return fresh_count

# ----------------------------------------------------------------------
# STRATEGY 2: O(N_Ranges * log N_Ranges + N_IDs * log N_Ranges) Optimized
# This is the correct, scalable solution using merging and binary search.
# ----------------------------------------------------------------------

def merge_ranges(ranges):
    """Merges overlapping and contiguous ranges into a minimal sorted list."""
    if not ranges:
        return []
    
    # 1. Sort the ranges by their start value
    ranges.sort(key=lambda x: x[0])
    
    merged = []
    current_start, current_end = ranges[0]
    
    # 2. Linear pass to merge
    for next_start, next_end in ranges[1:]:
        # If overlap or adjacent (e.g., 5-6 and 7-9)
        if next_start <= current_end + 1:
            current_end = max(current_end, next_end)
        else:
            # Found a gap
            merged.append((current_start, current_end))
            current_start, current_end = next_start, next_end
            
    # Add the final merged range
    merged.append((current_start, current_end))
    return merged

def binary_search_check(merged_ranges, id_val):
    """
    Uses binary search to find the correct range containing id_val.
    O(log N_Ranges).
    """
    low, high = 0, len(merged_ranges) - 1
    best_match_index = -1
    
    # Binary search to find the largest range start that is <= id_val
    while low <= high:
        mid = (low + high) // 2
        start, end = merged_ranges[mid]
        
        if start <= id_val:
            best_match_index = mid
            low = mid + 1 # Try to find an even larger start
        else:
            high = mid - 1
            
    if best_match_index == -1:
        return False
    
    # Final check: Does the ID fall within the end of that range?
    start, end = merged_ranges[best_match_index]
    return id_val <= end


def solve_optimized(fresh_ranges, available_ids):
    """Calculates the count using the Merge & Binary Search strategy."""
    
    # 1. Preprocessing: Merge
    merged = merge_ranges(fresh_ranges)
    
    # 2. Check each ID
    fresh_count = 0
    for id_val in available_ids:
        if binary_search_check(merged, id_val):
            fresh_count += 1
            
    return fresh_count

# ----------------------------------------------------
# 3. EXECUTION BLOCK
# ----------------------------------------------------

if __name__ == "__main__":
    
    fresh_ranges, available_ids = read_and_parse_input()
    
    if not fresh_ranges or not available_ids:
        print("Please ensure your puzzle input is in 'input.md' with correct formatting.")
        exit() 

    print("\n" + "="*70)
    print("🎄 Advent of Code - Day 5, Part 1 Results")
    print("="*70)

    # --- Run Strategies and Time Them ---
    
    # Strategy 1: Brute Force
    start_time_bf = time.perf_counter()
    result_bf = solve_brute_force(fresh_ranges, available_ids)
    time_bf = time.perf_counter() - start_time_bf
    print(f"| Brute Force (O(N_R * N_ID)): {result_bf}\t| Time: {time_bf:.6f}s")

    # Strategy 2: Optimized
    start_time_opt = time.perf_counter()
    result_opt = solve_optimized(fresh_ranges, available_ids)
    time_opt = time.perf_counter() - start_time_opt
    print(f"| Optimized (O(log N_R)): {result_opt}\t| Time: {time_opt:.6f}s")

    print("-" * 70)
    
    # Verification
    if result_bf == result_opt:
        print(f"✅ FINAL ANSWER (Verified): {result_opt} fresh ingredients.")
    else:
        print("⚠️ ERROR: Brute Force and Optimized results do not match. Check logic.")
        
    print("="*70 + "\n")
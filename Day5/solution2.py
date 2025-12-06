import os

# --- Input Reading and Parsing ---

def read_fresh_ranges(filename="input.md"):
    """Reads the fresh ID ranges from the input file."""
    if not os.path.exists(filename):
        print(f"Error: Input file '{filename}' not found.")
        return []
        
    with open(filename, 'r') as f:
        data = [line.strip() for line in f]

    # Stop parsing at the blank line or the end of the file
    range_lines = []
    for line in data:
        if line == '':
            break
        range_lines.append(line)

    # Parse Fresh ID Ranges (A-B)
    fresh_ranges = []
    for line in range_lines:
        if '-' in line:
            try:
                start, end = map(int, line.split('-'))
                fresh_ranges.append((start, end))
            except ValueError:
                continue
    return fresh_ranges

# ----------------------------------------------------------------------
# OPTIMIZED SOLUTION (O(N_Ranges * log N_Ranges))
# ----------------------------------------------------------------------

def merge_ranges(ranges):
    """Merges overlapping and contiguous ranges."""
    if not ranges:
        return []
    
    # 1. Sort the ranges by their start value
    ranges.sort(key=lambda x: x[0])
    
    merged = []
    current_start, current_end = ranges[0]
    
    # 2. Linear pass to merge
    for next_start, next_end in ranges[1:]:
        # If overlap or adjacent (next_start <= current_end + 1)
        if next_start <= current_end + 1:
            current_end = max(current_end, next_end)
        else:
            # Found a gap, finalize the current merged range and start a new one
            merged.append((current_start, current_end))
            current_start, current_end = next_start, next_end
            
    # Add the final merged range
    merged.append((current_start, current_end))
    return merged

def solve_day5_part2(fresh_ranges):
    """
    Calculates the total count of fresh IDs by merging ranges and summing lengths.
    """
    
    # 1. Merge the ranges (O(N log N))
    merged_ranges = merge_ranges(fresh_ranges)
    
    total_fresh_ids = 0
    
    # 2. Sum the length of the non-overlapping ranges (O(N))
    for start, end in merged_ranges:
        # Range length is (end - start + 1)
        total_fresh_ids += (end - start + 1)
            
    return total_fresh_ids

# ----------------------------------------------------
# 3. EXECUTION BLOCK
# ----------------------------------------------------

if __name__ == "__main__":
    
    fresh_ranges = read_fresh_ranges()
    
    if not fresh_ranges:
        print("Please ensure your puzzle input is in 'input.md' with correct formatting.")
        exit() 

    result = solve_day5_part2(fresh_ranges)

    print("\n" + "="*50)
    print("🎄 Advent of Code - Day 5, Part 2")
    print("="*50)
    print(f"Total Fresh Ingredient IDs: {result}")
    print("="*50 + "\n")
import math

def solve():
    # --- Input Parsing ---
    # We read the file and pad every line to the same width to make a perfect grid.
    with open('input.md', 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    if not lines:
        print("Input file is empty.")
        return

    max_width = max(len(line) for line in lines)
    grid = [line.ljust(max_width) for line in lines]

    # --- Step 1: Identify Blocks ---
    # We need to slice the grid vertically. 
    # A "separator" is a full column of spaces.
    
    # Transpose grid to work with columns easily
    # zip(*grid) takes the rows and pivots them into columns
    columns = list(zip(*grid))
    
    problem_blocks = []
    current_block_indices = []

    for idx, col in enumerate(columns):
        # Check if the column is entirely spaces
        if all(char == ' ' for char in col):
            if current_block_indices:
                problem_blocks.append(current_block_indices)
                current_block_indices = []
        else:
            current_block_indices.append(idx)
    
    # Capture the last block if it exists
    if current_block_indices:
        problem_blocks.append(current_block_indices)

    # --- Solvers ---

    def calculate_total(is_part_two=False):
        grand_total = 0
        
        for col_indices in problem_blocks:
            # Extract the slice of the grid for this problem
            # The operator is always in the last row of the block slice
            operator_row = grid[-1]
            operator_char = None
            
            # Find the operator in this block's width
            # We scan the last row within the column bounds of this block
            for c_idx in col_indices:
                if operator_row[c_idx] in ('+', '*'):
                    operator_char = operator_row[c_idx]
                    break
            
            if not operator_char:
                continue # Should not happen based on rules

            numbers = []
            
            if not is_part_two:
                # --- Part 1 Logic: Horizontal Rows ---
                # Iterate through rows, excluding the last one (operator row)
                for r_idx in range(len(grid) - 1):
                    # Construct the row string for this block
                    row_str = "".join(grid[r_idx][i] for i in col_indices)
                    clean_str = row_str.strip()
                    if clean_str:
                        numbers.append(int(clean_str))
            else:
                # --- Part 2 Logic: Vertical Columns (Right-to-Left) ---
                # We iterate the block's columns in reverse (Right to Left)
                reversed_indices = sorted(col_indices, reverse=True)
                
                for c_idx in reversed_indices:
                    # Construct the number from this column (Top to Bottom)
                    # Exclude the last row (operator)
                    col_digits = []
                    for r_idx in range(len(grid) - 1):
                        char = grid[r_idx][c_idx]
                        if char.isdigit():
                            col_digits.append(char)
                    
                    if col_digits:
                        # Join digits '1', '2', '3' -> 123
                        numbers.append(int("".join(col_digits)))

            # --- Perform Operation ---
            if not numbers:
                continue
                
            block_result = 0
            if operator_char == '+':
                block_result = sum(numbers)
            elif operator_char == '*':
                block_result = 1
                for n in numbers:
                    block_result *= n
            
            grand_total += block_result
            
        return grand_total

    # --- Output ---
    print(f"Part 1 Grand Total: {calculate_total(is_part_two=False)}")
    print(f"Part 2 Grand Total: {calculate_total(is_part_two=True)}")

if __name__ == "__main__":
    solve()
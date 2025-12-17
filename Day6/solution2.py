"""
Day 6: Trash Compactor - Part 2

Key insight: Cephalopod math reads RIGHT-TO-LEFT in columns.
- Each COLUMN represents one number (digits read top to bottom)
- Columns are processed right-to-left to build the list of numbers
- The operator is still at the bottom

Example:
 64
 23
314
+

Reading columns right-to-left:
- Rightmost column: "4", "3", "4" → 434... wait no
- Let me re-read...

Actually:
Column 0 (leftmost): " ", " ", "3" → 3
Column 1: "6", "2", "1" → 621
Column 2: "4", "3", "4" → 434

Reading RIGHT-TO-LEFT (col 2, col 1, col 0):
- Col 2 forms: 434
- Col 1 forms: 621
- Col 0 forms: 3

Hmm, that's not matching. Let me check the expected output again...
They say: "4 + 431 + 623 = 1058"

OH! Each column (from top to bottom) forms ONE number:
- Rightmost column has digits: 4 (row 0), 3 (row 1), 4 (row 2) → number 434
Wait, but they said 4, not 434.

Let me look at this more carefully. The problem area is:
 64
 23
314

If I look at column positions:
Position 0: ' ', ' ', '3'
Position 1: '6', '2', '1'
Position 2: '4', '3', '4'

Reading right-to-left (position 2, 1, 0):
- Position 2, top-to-bottom: '4', '3', '4' → but only the last row has all 3 digits

Actually, I think each column forms a number from top to bottom, ignoring spaces:
- Position 2: '4', '3', '4' top-to-bottom (ignoring operator row) = "434" → 434
  But they said the first number is 4...

Let me reconsider. Looking at " 64", " 23", "314":
If I extract columns character by character:
Col 0: ' ', ' ', '3'
Col 1: '6', '2', '1'
Col 2: '4', '3', '4'

Reading col 2 top-to-bottom: '4', '3', '4' forms "434"
Reading col 1 top-to-bottom: '6', '2', '1' forms "621"
Reading col 0 top-to-bottom: ' ', ' ', '3' forms "3"

But they said 4 + 431 + 623 = 1058

OH WAIT. Maybe the numbers in the original input are ALREADY in column format!
Let me re-read: "64" means column "6" and column "4"
Row 1: "64" → two columns
Row 2: "23" → two columns
Row 3: "314" → three columns

So:
Column 0 (leftmost of this problem): row1='6', row2='2', row3='3' → "623"
Column 1: row1='4', row2='3', row3='1' → "431"
Column 2 (rightmost): row1=' ', row2=' ', row3='4' → "4"

Reading RIGHT-TO-LEFT (col 2, col 1, col 0): 4, 431, 623
That matches!

So the algorithm is:
1. Identify problem boundaries (same as Part 1)
2. For each problem, extract its column range
3. Transpose to get columns
4. Read columns right-to-left
5. Each column forms a number (top to bottom, ignoring spaces and operator)
6. Calculate result
"""

def parse_worksheet(input_text):
    """Parse the worksheet and identify problem column ranges."""
    lines = input_text.strip().split('\n')

    if not lines:
        return []

    # Find the maximum line length
    max_len = max(len(line) for line in lines)

    # Pad all lines to the same length
    padded_lines = [line.ljust(max_len) for line in lines]

    # Find columns that are all spaces (separators)
    separator_columns = []
    for col_idx in range(max_len):
        column_chars = [padded_lines[row_idx][col_idx] for row_idx in range(len(padded_lines))]
        if all(char == ' ' for char in column_chars):
            separator_columns.append(col_idx)

    # Identify problem ranges (groups of non-separator columns)
    problem_ranges = []
    start = None

    for col_idx in range(max_len):
        if col_idx in separator_columns:
            if start is not None:
                # End of a problem
                problem_ranges.append((start, col_idx - 1))
                start = None
        else:
            if start is None:
                # Start of a problem
                start = col_idx

    # Don't forget the last problem
    if start is not None:
        problem_ranges.append((start, max_len - 1))

    # Extract the content for each problem
    problems = []
    for start_col, end_col in problem_ranges:
        problem_lines = []
        for line in padded_lines:
            problem_lines.append(line[start_col:end_col + 1])
        problems.append(problem_lines)

    return problems


def solve_problem_part2(problem_lines):
    """
    Solve a single math problem using Part 2 rules.

    Read columns right-to-left, each column forms one number.
    """
    if not problem_lines:
        return 0

    # Get the width (number of columns in this problem) and number of rows
    width = len(problem_lines[0]) if problem_lines else 0
    num_rows = len(problem_lines)

    # The operator is in the last row
    operator = None
    last_row = problem_lines[-1] if problem_lines else ""
    for char in last_row:
        if char in ['+', '*']:
            operator = char
            break

    # Extract numbers by reading columns right-to-left
    # EXCLUDE the last row (operator row) when reading digits
    numbers = []

    # Process columns from right to left
    for col_idx in range(width - 1, -1, -1):
        # Build number from this column, excluding the operator row
        number_str = ''
        for row_idx in range(num_rows - 1):  # Exclude last row
            if col_idx < len(problem_lines[row_idx]):
                char = problem_lines[row_idx][col_idx]
                if char.isdigit():
                    number_str += char

        if number_str:
            numbers.append(int(number_str))

    if not numbers or not operator:
        return 0

    # Calculate the result
    if operator == '+':
        result = sum(numbers)
    elif operator == '*':
        result = 1
        for num in numbers:
            result *= num
    else:
        result = 0

    return result


def solve(input_text):
    """Solve the entire worksheet and return the grand total."""
    problems = parse_worksheet(input_text)

    total = 0
    for i, problem in enumerate(problems):
        result = solve_problem_part2(problem)
        print(f"Problem {i+1}: {result}")
        total += result

    return total


if __name__ == "__main__":
    # Test with the example
    test_input = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """

    print("Testing Part 2 with example:")
    grand_total = solve(test_input)
    print(f"Grand Total: {grand_total}")
    print(f"Expected: 3263827")
    print(f"Test {'PASSED' if grand_total == 3263827 else 'FAILED'}!")
    print()

    # Solve with actual input
    try:
        with open('input.md', 'r') as f:
            content = f.read()

            if content.strip():
                print("\nSolving actual puzzle input:")
                result = solve(content)
                print(f"\nAnswer: {result}")
            else:
                print("\nNo puzzle input found. Add your input to input.md")
    except FileNotFoundError:
        print("\nNo input.md file found.")

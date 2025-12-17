"""
Day 6: Trash Compactor - Part 2 - Debug Version
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


def solve_problem_part2(problem_lines, problem_num):
    """
    Solve a single math problem using Part 2 rules.
    """
    if not problem_lines:
        return 0

    # Get the width (number of columns in this problem)
    width = len(problem_lines[0]) if problem_lines else 0
    num_rows = len(problem_lines)

    print(f"\n--- Problem {problem_num} ---")
    print(f"Problem area ({width} cols x {num_rows} rows):")
    for i, line in enumerate(problem_lines):
        print(f"  Row {i}: '{line}'")

    # The operator should be in the last row
    operator = None
    last_row = problem_lines[-1] if problem_lines else ""
    for char in last_row:
        if char in ['+', '*']:
            operator = char
            break

    print(f"Operator: {operator}")

    # Extract numbers by reading columns right-to-left
    # But EXCLUDE the last row (operator row) when reading digits
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
            number = int(number_str)
            numbers.append(number)
            print(f"  Col {col_idx}: '{number_str}' → {number}")

    print(f"Numbers (right-to-left): {numbers}")

    if not numbers or not operator:
        return 0

    # Calculate the result
    if operator == '+':
        result = sum(numbers)
        print(f"Calculation: {' + '.join(map(str, numbers))} = {result}")
    elif operator == '*':
        result = 1
        for num in numbers:
            result *= num
        print(f"Calculation: {' * '.join(map(str, numbers))} = {result}")
    else:
        result = 0

    return result


# Test with the example
test_input = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """

print("="*60)
print("Testing Part 2 with example:")
print("="*60)
problems = parse_worksheet(test_input)
total = 0
for i, problem in enumerate(problems):
    result = solve_problem_part2(problem, i+1)
    total += result

print(f"\n{'='*60}")
print(f"Grand Total: {total}")
print(f"Expected: 3263827")
print(f"Test {'PASSED' if total == 3263827 else 'FAILED'}!")

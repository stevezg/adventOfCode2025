"""
Day 6: Trash Compactor - Part 1

Solve the cephalopod math worksheet by:
1. Parsing vertical math problems
2. Each problem is in a group of columns
3. Columns of all spaces separate problems
4. Calculate each problem and sum all results
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


def solve_problem(problem_lines):
    """
    Solve a single math problem.

    Args:
        problem_lines: List of strings, each representing one row of the problem

    Returns:
        The result of the calculation
    """
    # Extract all numbers and the operator
    numbers = []
    operator = None

    for line in problem_lines:
        tokens = line.strip().split()
        for token in tokens:
            if token in ['+', '*']:
                operator = token
            else:
                try:
                    numbers.append(int(token))
                except ValueError:
                    pass

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
        result = solve_problem(problem)
        print(f"Problem {i+1}: {result}")
        total += result

    return total


if __name__ == "__main__":
    # Test with the example
    test_input = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """

    print("Testing with example:")
    grand_total = solve(test_input)
    print(f"Grand Total: {grand_total}")
    print(f"Expected: 4277556")
    print(f"Test {'PASSED' if grand_total == 4277556 else 'FAILED'}!")
    print()

    # Solve with actual input
    try:
        with open('input.md', 'r') as f:
            content = f.read()
            # Skip markdown header if present
            lines = content.split('\n')
            if lines and lines[0].startswith('#'):
                # Find where actual content starts (after headers)
                start_idx = 0
                for i, line in enumerate(lines):
                    if line.strip() and not line.startswith('#'):
                        start_idx = i
                        break
                content = '\n'.join(lines[start_idx:])

            if content.strip() and not content.strip().startswith('Paste'):
                print("\nSolving actual puzzle input:")
                result = solve(content)
                print(f"\nAnswer: {result}")
            else:
                print("\nNo puzzle input found. Add your input to input.md")
    except FileNotFoundError:
        print("\nNo input.md file found.")

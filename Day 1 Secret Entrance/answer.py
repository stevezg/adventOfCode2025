def solve_safe_password(instructions):
    """ 
    calculate how many times the dial points to 0 during rotations
    args: 
        instructions: list of rotation strings like ['L32, 'R15, ...]

    Returns: 
        the password (count of times dial points to 0)
    """
    position = 50 # starting point
    zero_count = 0 # how many times we land on zero

    # proccess each instruction
    for instruction in instructions:
        # parse the instruction
        direction = instruction[0] #  'L' or 'R'
        distance = int(instruction[1:]) # the number part

        # move the dial
        if direction == 'L':
            position = (position - distance) % 100
        else:
            position = (position + distance) % 100
        
        if position == 0:
            zero_count += 1

    return zero_count

with open('input.md', 'r') as f:
    instructions = [line.strip() for line in f.readlines()]

password = solve_safe_password(instructions)
print(f"the password is: {password}")
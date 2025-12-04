def solve_safe_part2():
    current_pos = 50
    total_hits = 0
    
    # Reading the input (assuming input.md contains the raw lines)
    with open('input.md', 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    
    for instruction in lines:
        if not instruction: continue
        
        direction = instruction[0]
        amount = int(instruction[1:])
        
        # 1. Calculate distance to the *next* 0
        dist_to_0 = 0
        
        if current_pos == 0:
            dist_to_0 = 100 # If at 0, full circle needed to click 0 again
        elif direction == 'R':
            dist_to_0 = 100 - current_pos
        elif direction == 'L':
            dist_to_0 = current_pos
            
        # 2. Check intersections
        if amount >= dist_to_0:
            # We hit 0 at least once
            hits = 1
            
            # How many FULL circles (100s) are left after that first hit?
            remaining = amount - dist_to_0
            hits += remaining // 100
            
            total_hits += hits
            
        # 3. Update Position (Standard Part 1 logic)
        if direction == 'R':
            current_pos = (current_pos + amount) % 100
        elif direction == 'L':
            current_pos = (current_pos - amount) % 100
            
    print(f"The Part 2 password is: {total_hits}")

if __name__ == "__main__":
    solve_safe_part2()
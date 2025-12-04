def solve():
    with open("input.md", "r") as f:
        rotations = [line.strip() for line in f if line.strip()]
    
    position = 50
    zero_count = 0
    
    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])
        
        # Calculate how many times we land on 0 during this rotation
        # After k clicks: position ± k (mod 100) == 0
        # For L: (position - k) % 100 == 0  =>  k ≡ position (mod 100)
        # For R: (position + k) % 100 == 0  =>  k ≡ -position ≡ 100-position (mod 100)
        
        if position == 0:
            # Starting at 0, we hit 0 again every 100 clicks
            zero_count += distance // 100
        else:
            # First zero crossing
            first_zero = position if direction == 'L' else (100 - position)
            if distance >= first_zero:
                zero_count += 1 + (distance - first_zero) // 100
        
        # Update position
        if direction == 'L':
            position = (position - distance) % 100
        else:
            position = (position + distance) % 100
    
    print(f"Password (Part 2): {zero_count}")

if __name__ == "__main__":
    solve()
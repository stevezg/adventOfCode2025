import os
import sys

def parse_shapes(filename):
    """Parse the present shapes from input file."""
    shapes = {}
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if ':' in line and line[0].isdigit() and 'x' not in line:
            # Parse shape index
            shape_idx = int(line.split(':')[0])
            shape_lines = []
            i += 1
            
            # Read shape lines until we hit another shape or region
            while i < len(lines):
                line = lines[i].strip()
                if not line:
                    i += 1
                    continue
                # Check if this is a new shape or region
                if ':' in line and (line[0].isdigit() or 'x' in line):
                    break
                if line and 'x' not in line:
                    shape_lines.append(line)
                i += 1
            
            # Convert shape to coordinates
            if shape_lines:
                shape_coords = []
                for r, row in enumerate(shape_lines):
                    for c, char in enumerate(row):
                        if char == '#':
                            shape_coords.append((r, c))
                
                if shape_coords:
                    shapes[shape_idx] = shape_coords
        else:
            i += 1
    
    return shapes

def parse_regions(filename):
    """Parse the regions from input file."""
    regions = []
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line or (':' in line and line[0].isdigit() and 'x' not in line):
            continue
        
        if 'x' in line:
            # Parse region: "WxH: count1 count2 ..."
            parts = line.split(':')
            size_part = parts[0].strip()
            width, height = map(int, size_part.split('x'))
            counts = list(map(int, parts[1].strip().split()))
            regions.append((width, height, counts))
    
    return regions

def normalize_shape(shape_coords):
    """Normalize shape by shifting to start at (0,0)."""
    if not shape_coords:
        return []
    min_r = min(r for r, c in shape_coords)
    min_c = min(c for r, c in shape_coords)
    return [(r - min_r, c - min_c) for r, c in shape_coords]

def rotate_90_cw(shape_coords):
    """Rotate shape 90 degrees clockwise."""
    if not shape_coords:
        return []
    # 90 deg CW: (r, c) -> (c, max_r - r)
    max_r = max(r for r, c in shape_coords)
    rotated = [(c, max_r - r) for r, c in shape_coords]
    return normalize_shape(rotated)

def flip_horizontal(shape_coords):
    """Flip shape horizontally."""
    if not shape_coords:
        return []
    max_c = max(c for r, c in shape_coords)
    return normalize_shape([(r, max_c - c) for r, c in shape_coords])

def flip_vertical(shape_coords):
    """Flip shape vertically."""
    if not shape_coords:
        return []
    max_r = max(r for r, c in shape_coords)
    return normalize_shape([(max_r - r, c) for r, c in shape_coords])

def get_all_variants(shape_coords):
    """Get all unique rotations and flips of a shape."""
    variants = set()
    current = shape_coords
    
    # Generate all rotations (0, 90, 180, 270)
    for _ in range(4):
        current_normalized = tuple(sorted(normalize_shape(current)))
        variants.add(current_normalized)
        
        # Try horizontal flip
        flipped_h = flip_horizontal(current)
        variants.add(tuple(sorted(flipped_h)))
        
        # Try vertical flip
        flipped_v = flip_vertical(current)
        variants.add(tuple(sorted(flipped_v)))
        
        # Try both flips
        flipped_both = flip_vertical(flip_horizontal(current))
        variants.add(tuple(sorted(flipped_both)))
        
        # Rotate for next iteration
        current = rotate_90_cw(current)
    
    # Convert back to list of coordinates
    return [list(v) for v in variants]

def can_place_shape(grid, shape_coords, start_r, start_c):
    """Check if shape can be placed at (start_r, start_c) in grid."""
    height, width = len(grid), len(grid[0])
    
    for dr, dc in shape_coords:
        r, c = start_r + dr, start_c + dc
        if r < 0 or r >= height or c < 0 or c >= width:
            return False
        if grid[r][c] != '.':
            return False
    
    return True

def place_shape(grid, shape_coords, start_r, start_c):
    """Place shape on grid (modifies grid in place)."""
    for dr, dc in shape_coords:
        r, c = start_r + dr, start_c + dc
        grid[r][c] = '#'

def remove_shape(grid, shape_coords, start_r, start_c):
    """Remove shape from grid (modifies grid in place)."""
    for dr, dc in shape_coords:
        r, c = start_r + dr, start_c + dc
        grid[r][c] = '.'

def solve_packing(width, height, shape_counts, shape_variants_dict):
    """
    Try to pack all shapes into the grid using backtracking.
    Returns True if all shapes can be placed.
    """
    # Early check: total area must fit
    total_area = width * height
    required_area = 0
    for shape_idx, count in enumerate(shape_counts):
        shape_size = len(shape_variants_dict[shape_idx][0])
        required_area += shape_size * count
    if required_area > total_area:
        return False
    
    grid = [['.' for _ in range(width)] for _ in range(height)]
    
    # Create list of shapes to place
    shapes_to_place = []
    for shape_idx, count in enumerate(shape_counts):
        for _ in range(count):
            shapes_to_place.append(shape_idx)
    
    if not shapes_to_place:
        return True
    
    # Sort shapes by size (larger first for better pruning)
    def get_shape_size(idx):
        return len(shape_variants_dict[idx][0])
    
    shapes_to_place.sort(key=get_shape_size, reverse=True)
    
    # Precompute valid positions for each variant to avoid repeated checks
    def get_valid_positions(variant):
        positions = []
        for r in range(height):
            for c in range(width):
                if can_place_shape(grid, variant, r, c):
                    positions.append((r, c))
        return positions
    
    def backtrack(idx):
        if idx == len(shapes_to_place):
            return True
        
        shape_idx = shapes_to_place[idx]
        variants = shape_variants_dict[shape_idx]
        
        # Try placing this shape in all possible positions with all variants
        # Try variants in order, and positions from top-left first
        for variant in variants:
            # Get valid positions for this variant
            positions = get_valid_positions(variant)
            
            for r, c in positions:
                # Place shape
                place_shape(grid, variant, r, c)
                
                # Recurse
                if backtrack(idx + 1):
                    return True
                
                # Remove shape (backtrack)
                remove_shape(grid, variant, r, c)
        
        return False
    
    return backtrack(0)

def solve():
    """Main solve function."""
    filename = "input.txt"
    
    if not os.path.exists(filename):
        print(f"Error: Input file '{filename}' not found.")
        return
    
    # Parse shapes
    shapes = parse_shapes(filename)
    print(f"Parsed {len(shapes)} shapes")
    
    # Generate all variants for each shape
    shape_variants_dict = {}
    for shape_idx, shape_coords in shapes.items():
        variants = get_all_variants(shape_coords)
        shape_variants_dict[shape_idx] = variants
        print(f"Shape {shape_idx}: {len(variants)} unique variants")
    
    # Parse regions
    regions = parse_regions(filename)
    print(f"Found {len(regions)} regions\n")
    
    # Check each region
    count = 0
    for i, (width, height, shape_counts) in enumerate(regions):
        if (i + 1) % 100 == 0:
            print(f"Progress: {i+1}/{len(regions)} regions checked, {count} fit so far", flush=True)
        
        if solve_packing(width, height, shape_counts, shape_variants_dict):
            count += 1
    
    print(f"\nTotal regions that can fit all presents: {count}")

if __name__ == "__main__":
    solve()

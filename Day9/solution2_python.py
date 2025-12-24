import sys
from math import gcd

# Read input
data = sys.stdin.read().strip().split('\n')
points = []
for line in data:
    x, y = map(int, line.split(','))
    points.append((x, y))
n = len(points)

def shoelace(poly):
    if len(poly) < 3:
        return 0
    s = 0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return abs(s)

def compute_lattice(poly):
    if len(poly) < 3:
        return 0
    sum2 = shoelace(poly)
    v = len(poly)
    boundary_add = 0
    for i in range(v):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % v]
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        g = gcd(dx, dy)
        boundary_add += g - 1
    b = boundary_add + v
    return (sum2 + b) // 2 + 1

def clip_left(poly, xmin):
    if not poly:
        return []
    output = []
    prev = poly[-1]
    prev_x, prev_y = prev
    for curr in poly:
        curr_x, curr_y = curr
        prev_in = prev_x >= xmin
        curr_in = curr_x >= xmin
        if curr_in:
            if not prev_in:
                if curr_x == prev_x:
                    inter_y = prev_y
                else:
                    t = (xmin - prev_x) / (curr_x - prev_x)
                    inter_y = prev_y + t * (curr_y - prev_y)
                output.append((xmin, int(round(inter_y))))
            output.append(curr)
        elif prev_in:
            if curr_x == prev_x:
                inter_y = prev_y
            else:
                t = (xmin - prev_x) / (curr_x - prev_x)
                inter_y = prev_y + t * (curr_y - prev_y)
            output.append((xmin, int(round(inter_y))))
        prev = (curr_x, curr_y)
        prev_x, prev_y = prev
    return output

def clip_right(poly, xmax):
    if not poly:
        return []
    output = []
    prev = poly[-1]
    prev_x, prev_y = prev
    for curr in poly:
        curr_x, curr_y = curr
        prev_in = prev_x <= xmax
        curr_in = curr_x <= xmax
        if curr_in:
            if not prev_in:
                if curr_x == prev_x:
                    inter_y = prev_y
                else:
                    t = (xmax - prev_x) / (curr_x - prev_x)
                    inter_y = prev_y + t * (curr_y - prev_y)
                output.append((xmax, int(round(inter_y))))
            output.append(curr)
        elif prev_in:
            if curr_x == prev_x:
                inter_y = prev_y
            else:
                t = (xmax - prev_x) / (curr_x - prev_x)
                inter_y = prev_y + t * (curr_y - prev_y)
            output.append((xmax, int(round(inter_y))))
        prev = (curr_x, curr_y)
        prev_x, prev_y = prev
    return output

def clip_bottom(poly, ymin):
    if not poly:
        return []
    output = []
    prev = poly[-1]
    prev_x, prev_y = prev
    for curr in poly:
        curr_x, curr_y = curr
        prev_in = prev_y >= ymin
        curr_in = curr_y >= ymin
        if curr_in:
            if not prev_in:
                if curr_y == prev_y:
                    inter_x = prev_x
                else:
                    t = (ymin - prev_y) / (curr_y - prev_y)
                    inter_x = prev_x + t * (curr_x - prev_x)
                output.append((int(round(inter_x)), ymin))
            output.append(curr)
        elif prev_in:
            if curr_y == prev_y:
                inter_x = prev_x
            else:
                t = (ymin - prev_y) / (curr_y - prev_y)
                inter_x = prev_x + t * (curr_x - prev_x)
            output.append((int(round(inter_x)), ymin))
        prev = (curr_x, curr_y)
        prev_x, prev_y = prev
    return output

def clip_top(poly, ymax):
    if not poly:
        return []
    output = []
    prev = poly[-1]
    prev_x, prev_y = prev
    for curr in poly:
        curr_x, curr_y = curr
        prev_in = prev_y <= ymax
        curr_in = curr_y <= ymax
        if curr_in:
            if not prev_in:
                if curr_y == prev_y:
                    inter_x = prev_x
                else:
                    t = (ymax - prev_y) / (curr_y - prev_y)
                    inter_x = prev_x + t * (curr_x - prev_x)
                output.append((int(round(inter_x)), ymax))
            output.append(curr)
        elif prev_in:
            if curr_y == prev_y:
                inter_x = prev_x
            else:
                t = (ymax - prev_y) / (curr_y - prev_y)
                inter_x = prev_x + t * (curr_x - prev_x)
            output.append((int(round(inter_x)), ymax))
        prev = (curr_x, curr_y)
        prev_x, prev_y = prev
    return output

def clip_polygon_to_rect(poly, x_min, x_max, y_min, y_max):
    poly = clip_left(poly, x_min)
    poly = clip_right(poly, x_max)
    poly = clip_bottom(poly, y_min)
    poly = clip_top(poly, y_max)
    return poly

max_area = 0
for i in range(n):
    for j in range(i + 1, n):
        px1, py1 = points[i]
        px2, py2 = points[j]
        x1 = min(px1, px2)
        x2 = max(px1, px2)
        y1 = min(py1, py2)
        y2 = max(py1, py2)
        if x1 == x2 or y1 == y2:
            continue
        rect_lattice = (x2 - x1 + 1) * (y2 - y1 + 1)
        clipped = clip_polygon_to_rect(points, x1, x2, y1, y2)
        inter_lattice = compute_lattice(clipped)
        if inter_lattice == rect_lattice:
            max_area = max(max_area, rect_lattice)

print(max_area)
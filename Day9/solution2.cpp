#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <fstream>
#include <algorithm>
#include <cmath>

using namespace std;

struct Point {
    long long x, y;
};

struct VEdge {
    long long x;
    long long y_min, y_max;
};

struct HEdge {
    long long y;
    long long x_min, x_max;
};

// Parse input handling x,y or space separated formats
vector<Point> parseInput(const string& filename) {
    vector<Point> points;
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Error: Could not open " << filename << endl;
        exit(1);
    }

    string line;
    while (getline(file, line)) {
        // Replace commas with spaces
        for (char &c : line) if (c == ',') c = ' ';
        
        stringstream ss(line);
        long long x, y;
        while (ss >> x >> y) {
            points.push_back({x, y});
        }
    }
    return points;
}

int main() {
    // 1. Load Data
    vector<Point> points = parseInput("input.txt");
    int n = points.size();
    
    if (n < 4) {
        cout << "Not enough points to form a polygon." << endl;
        return 0;
    }

    // 2. Build Polygon Edges
    vector<VEdge> v_edges;
    vector<HEdge> h_edges;

    for (int i = 0; i < n; ++i) {
        Point p1 = points[i];
        Point p2 = points[(i + 1) % n];

        if (p1.x == p2.x) {
            v_edges.push_back({p1.x, min(p1.y, p2.y), max(p1.y, p2.y)});
        } else if (p1.y == p2.y) {
            h_edges.push_back({p1.y, min(p1.x, p2.x), max(p1.x, p2.x)});
        }
    }

    // 3. Sort edges for Binary Search
    sort(v_edges.begin(), v_edges.end(), [](const VEdge& a, const VEdge& b) {
        return a.x < b.x;
    });
    sort(h_edges.begin(), h_edges.end(), [](const HEdge& a, const HEdge& b) {
        return a.y < b.y;
    });

    long long max_area = 0;

    // 4. Iterate all pairs of Red Tiles
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            long long x1 = points[i].x;
            long long y1 = points[i].y;
            long long x2 = points[j].x;
            long long y2 = points[j].y;

            // Form a rectangle (even if width/height is 0, it's 1 tile wide/tall)
            long long width = abs(x1 - x2);
            long long height = abs(y1 - y2);
            
            // CORRECTION: Inclusive Area Calculation (Grid Tiles)
            long long area = (width + 1) * (height + 1);

            if (area <= max_area) continue;

            long long left = min(x1, x2);
            long long right = max(x1, x2);
            long long bottom = min(y1, y2);
            long long top = max(y1, y2);

            bool invalid = false;

            // --- CHECK A: Vertical Edge Intersection ---
            // Look for polygon edges strictly INSIDE the x-range (left, right)
            auto it_v = upper_bound(v_edges.begin(), v_edges.end(), left, 
                [](long long val, const VEdge& e) { return val < e.x; });
            
            for (; it_v != v_edges.end(); ++it_v) {
                if (it_v->x >= right) break; 
                // Check if this vertical edge cuts through the rectangle's Y range
                // Intersection of (y_min, y_max) and (bottom, top)
                // We use strict > bottom and < top to ensure we don't count touching boundaries
                if (it_v->y_min < top && it_v->y_max > bottom) {
                    invalid = true;
                    break;
                }
            }
            if (invalid) continue;

            // --- CHECK B: Horizontal Edge Intersection ---
            auto it_h = upper_bound(h_edges.begin(), h_edges.end(), bottom, 
                [](long long val, const HEdge& e) { return val < e.y; });

            for (; it_h != h_edges.end(); ++it_h) {
                if (it_h->y >= top) break;
                if (it_h->x_min < right && it_h->x_max > left) {
                    invalid = true;
                    break;
                }
            }
            if (invalid) continue;

            // --- CHECK C: Enclosure (Point in Polygon) ---
            // Ray Casting from the center-bottom of the rectangle.
            // Conceptual Ray Origin: x = left + epsilon, y = bottom + 0.5
            // Actually, since we proved no edges are *inside* (left, right),
            // we can cast a ray from anywhere in that X range.
            // We check how many vertical edges are to the RIGHT (x >= right).
            
            // We need to count edges that cover the Y-slice [bottom, bottom+1]
            // i.e., edge.y_min <= bottom AND edge.y_max > bottom
            
            // Start searching for edges at x >= right (boundary is included in ray check)
            auto it_ray = lower_bound(v_edges.begin(), v_edges.end(), right, 
                [](const VEdge& e, long long val) { return e.x < val; });
             
             long long intersections = 0;
             for (; it_ray != v_edges.end(); ++it_ray) {
                 // Does this edge cross the line y = bottom + 0.5?
                 if (it_ray->y_min <= bottom && it_ray->y_max > bottom) {
                     intersections++;
                 }
             }

             // Odd intersections = Inside
             if (intersections % 2 != 0) {
                 max_area = area;
             }
        }
    }

    cout << "Part 2 Largest Area: " << max_area << endl;

    return 0;
}
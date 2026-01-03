#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Copy the functions from the main solution
bool isOnBoundary(long long testx, long long testy, const vector<pair<long long, long long>>& reds) {
    int n = reds.size();
    for (int i = 0; i < n; ++i) {
        int j = (i + 1) % n;
        long long x1 = reds[i].first, y1 = reds[i].second;
        long long x2 = reds[j].first, y2 = reds[j].second;

        if (x1 == x2) {
            // Vertical line
            if (testx == x1 && testy >= min(y1, y2) && testy <= max(y1, y2)) {
                return true;
            }
        } else if (y1 == y2) {
            // Horizontal line
            if (testy == y1 && testx >= min(x1, x2) && testx <= max(x1, x2)) {
                return true;
            }
        }
    }
    return false;
}

bool isInsidePolygon(long long testx, long long testy, const vector<pair<long long, long long>>& reds) {
    int n = reds.size();
    int winding = 0;

    for (int i = 0; i < n; ++i) {
        int j = (i + 1) % n;
        long long x1 = reds[i].first, y1 = reds[i].second;
        long long x2 = reds[j].first, y2 = reds[j].second;

        if ((y1 <= testy && y2 > testy) || (y1 > testy && y2 <= testy)) {
            double x_intersect = x1 + (double)(x2 - x1) * (testy - y1) / (y2 - y1);
            if (x_intersect > testx) {
                winding++;
            }
        }
    }

    return (winding % 2) == 1;
}

bool isValidTile(long long x, long long y, const vector<pair<long long, long long>>& reds) {
    // Check if it's a red tile
    for (auto& p : reds) {
        if (p.first == x && p.second == y) return true;
    }

    // Check if it's on boundary or inside
    return isOnBoundary(x, y, reds) || isInsidePolygon(x, y, reds);
}

bool isRectangleValid(long long x1, long long y1, long long x2, long long y2,
                     const vector<pair<long long, long long>>& reds) {
    // Check all points on the rectangle boundary
    // Top edge
    for (long long x = x1; x <= x2; ++x) {
        if (!isValidTile(x, y1, reds)) return false;
    }
    // Bottom edge
    for (long long x = x1; x <= x2; ++x) {
        if (!isValidTile(x, y2, reds)) return false;
    }
    // Left edge (excluding corners already checked)
    for (long long y = y1 + 1; y < y2; ++y) {
        if (!isValidTile(x1, y, reds)) return false;
    }
    // Right edge (excluding corners already checked)
    for (long long y = y1 + 1; y < y2; ++y) {
        if (!isValidTile(x2, y, reds)) return false;
    }

    return true;
}

int main() {
    // Example from the problem: 7,1 11,1 11,7 9,7 9,5 2,5 2,3 7,3
    vector<pair<long long, long long>> reds = {
        {7,1}, {11,1}, {11,7}, {9,7}, {9,5}, {2,5}, {2,3}, {7,3}
    };

    cout << "Testing example with " << reds.size() << " red tiles" << endl;

    long long max_area = 0;

    for (size_t i = 0; i < reds.size(); ++i) {
        for (size_t j = i + 1; j < reds.size(); ++j) {
            long long x1 = reds[i].first, y1 = reds[i].second;
            long long x2 = reds[j].first, y2 = reds[j].second;

            long long left = min(x1, x2), right = max(x1, x2);
            long long top = min(y1, y2), bottom = max(y1, y2);

            long long area = (right - left + 1) * (bottom - top + 1);

            if (isRectangleValid(left, top, right, bottom, reds)) {
                if (area > max_area) {
                    max_area = area;
                    cout << "Valid rectangle: (" << left << "," << top << ") to (" << right << "," << bottom << ") area " << area << endl;
                }
            }
        }
    }

    cout << "Max area: " << max_area << endl;
    return 0;
}




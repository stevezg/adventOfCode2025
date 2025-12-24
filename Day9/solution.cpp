#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <cstdlib>
#include <algorithm>

using namespace std;

int main() {
    ifstream infile("input.txt");
    if (!infile) {
        cerr << "Error opening input.txt" << endl;
        return 1;
    }

    vector<pair<int, int>> points;
    string line;
    while (getline(infile, line)) {
        if (line.empty()) continue;
        stringstream ss(line);
        int x, y;
        char comma;
        ss >> x >> comma >> y;
        if (ss.fail()) {
            cerr << "Invalid line: " << line << endl;
            continue;
        }
        points.emplace_back(x, y);
    }

    size_t n = points.size();
    long long max_area = 0;
    for (size_t i = 0; i < n; ++i) {
        for (size_t j = i + 1; j < n; ++j) {
            int dx = abs(points[i].first - points[j].first);
            int dy = abs(points[i].second - points[j].second);
            long long area = (dx + 1LL) * (dy + 1);
            if (area > max_area) {
                max_area = area;
            }
        }
    }

    cout << max_area << endl;
    return 0;
}
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <queue>
#include <map>
#include <string>
#include <cctype>

using namespace std;

// Machine structure
struct Machine {
    vector<vector<int>> buttons;
    vector<int> target;
};

// Parse a line like "(1,3)" into vector<int>
vector<int> parseButton(const string &s) {
    vector<int> res;
    string tmp;
    for (char c : s) {
        if (isdigit(c)) tmp += c;
        else if (!tmp.empty()) {
            res.push_back(stoi(tmp));
            tmp.clear();
        }
    }
    if (!tmp.empty()) res.push_back(stoi(tmp));
    return res;
}

// Parse a line like "{3,5,4,7}" into vector<int>
vector<int> parseTarget(const string &s) {
    vector<int> res;
    string tmp;
    for (char c : s) {
        if (isdigit(c)) tmp += c;
        else if (!tmp.empty()) {
            res.push_back(stoi(tmp));
            tmp.clear();
        }
    }
    if (!tmp.empty()) res.push_back(stoi(tmp));
    return res;
}

// BFS to find minimal button presses for one machine
int minPresses(const Machine &m) {
    int n = m.target.size();
    queue<pair<vector<int>, int>> q;
    map<vector<int>, int> dist;

    vector<int> start(n, 0);
    q.push({start, 0});
    dist[start] = 0;

    while (!q.empty()) {
        auto curr_pair = q.front(); q.pop();
        vector<int> curr = curr_pair.first;
        int presses = curr_pair.second;

        if (curr == m.target) return presses;

        for (auto &btn : m.buttons) {
            vector<int> next = curr;
            for (int idx : btn) next[idx]++;
            if (dist.find(next) == dist.end() || dist[next] > presses + 1) {
                dist[next] = presses + 1;
                q.push({next, presses + 1});
            }
        }
    }

    return -1; // unreachable
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " input.txt\n";
        return 1;
    }

    ifstream fin(argv[1]);
    if (!fin) {
        cerr << "Cannot open file: " << argv[1] << "\n";
        return 1;
    }

    string line;
    vector<Machine> machines;
    while (getline(fin, line)) {
        if (line.empty()) continue;

        Machine m;
        stringstream ss(line);
        string token;
        vector<string> tokens;

        // Split line by spaces
        while (ss >> token) tokens.push_back(token);

        if (tokens.size() < 2) continue;

        // Last token is target counters
        m.target = parseTarget(tokens.back());

        // All other tokens (except first machine diagram) are buttons
        for (size_t i = 1; i + 1 < tokens.size(); i++) {
            m.buttons.push_back(parseButton(tokens[i]));
        }

        machines.push_back(m);
    }

    int total = 0;
    for (auto &m : machines) {
        int presses = minPresses(m);
        if (presses == -1) {
            cout << "Machine unreachable!\n";
        } else {
            total += presses;
        }
    }

    cout << "Fewest button presses: " << total << "\n";
}

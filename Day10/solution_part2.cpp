#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <queue>
#include <unordered_set>
#include <tuple>
#include <string>
#include <limits>
#include <regex>

using namespace std;

// State representation: tuple of counter values
using State = vector<int>;

// Hash function for vector<int> to use in unordered_set
struct hash_vector {
    size_t operator()(const vector<int>& v) const {
        size_t seed = v.size();
        for (auto& i : v) {
            seed ^= i + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        }
        return seed;
    }
};

// Parse a single machine line for Part 2
pair<vector<vector<int>>, vector<int>> parse_machine_part2(const string& line) {
    vector<vector<int>> buttons;
    vector<int> targets;

    // Use regex to find button and target parts
    regex button_regex(R"(\([^\)]+\))");
    regex target_regex(R"(\{[^\}]+\})");

    smatch match;
    string::const_iterator search_start(line.cbegin());

    // Find all buttons
    while (regex_search(search_start, line.cend(), match, button_regex)) {
        string button_str = match[0].str();
        button_str = button_str.substr(1, button_str.size() - 2); // Remove parentheses

        vector<int> button;
        if (!button_str.empty()) {
            stringstream ss(button_str);
            string token;
            while (getline(ss, token, ',')) {
                button.push_back(stoi(token));
            }
        }
        buttons.push_back(button);
        search_start = match.suffix().first;
    }

    // Find target
    if (regex_search(line, match, target_regex)) {
        string target_str = match[0].str();
        target_str = target_str.substr(1, target_str.size() - 2); // Remove braces

        stringstream ss(target_str);
        string token;
        while (getline(ss, token, ',')) {
            targets.push_back(stoi(token));
        }
    }

    return {buttons, targets};
}

int solve_machine_part2_bounded(const vector<vector<int>>& buttons, const vector<int>& targets, int max_presses_per_button = 50) {
    int n = targets.size(); // number of counters
    int m = buttons.size(); // number of buttons

    State start_state(n, 0);
    State target_state = targets;

    // BFS queue: tuple of (current_state, presses_used, press_counts)
    using QueueItem = tuple<State, int, vector<int>>;
    queue<QueueItem> q;
    unordered_set<State, hash_vector> visited;

    q.push(make_tuple(start_state, 0, vector<int>(m, 0)));
    visited.insert(start_state);

    int best_cost = numeric_limits<int>::max();

    while (!q.empty()) {
        auto [current_state, presses, press_counts] = q.front();
        q.pop();

        if (current_state == target_state) {
            best_cost = min(best_cost, presses);
            continue;
        }

        if (presses >= best_cost) {
            continue;
        }

        // Try pressing each button
        for (int button_idx = 0; button_idx < m; ++button_idx) {
            if (press_counts[button_idx] >= max_presses_per_button) {
                continue;
            }

            State new_state = current_state;
            bool valid = true;

            // Apply button press
            for (int counter_idx : buttons[button_idx]) {
                if (counter_idx < n) {
                    new_state[counter_idx] += 1;
                    // Prune if we exceed the target
                    if (new_state[counter_idx] > targets[counter_idx]) {
                        valid = false;
                        break;
                    }
                }
            }

            if (!valid) {
                continue;
            }

            vector<int> new_press_counts = press_counts;
            new_press_counts[button_idx] += 1;

            if (visited.find(new_state) == visited.end()) {
                visited.insert(new_state);
                q.push(make_tuple(new_state, presses + 1, new_press_counts));
            }
        }
    }

    return (best_cost != numeric_limits<int>::max()) ? best_cost : -1;
}

int main(int argc, char* argv[]) {
    string filename;
    if (argc > 1) {
        filename = argv[1];
    } else {
        filename = "input.txt";
    }

    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Error opening file: " << filename << endl;
        return 1;
    }

    string line;
    long long total_presses = 0;
    int machine_count = 0;

    while (getline(file, line)) {
        if (line.empty()) continue;

        auto [buttons, targets] = parse_machine_part2(line);
        int min_presses = solve_machine_part2_bounded(buttons, targets);

        if (min_presses == -1) {
            cout << "Machine " << targets.size() << " counters, " << buttons.size()
                 << " buttons: No solution found (try increasing max_presses_per_button)" << endl;
            continue;
        }

        total_presses += min_presses;
        cout << "Machine " << targets.size() << " counters, " << buttons.size()
             << " buttons: " << min_presses << " presses" << endl;
        machine_count++;
    }

    cout << "Total minimum presses: " << total_presses << endl;
    cout << "Processed " << machine_count << " machines" << endl;

    return 0;
}

# Day 10: Factory - Indicator Light Configuration

This problem involves configuring indicator lights on factory machines by pressing buttons that toggle specific lights, finding the minimum number of button presses to reach the target configuration.

## Problem Analysis

Each machine has:
- A target configuration of indicator lights (shown as `[.#.#.]`)
- Multiple buttons that toggle specific lights (shown as `(0,2,4)`)
- All lights start off (0)

The goal is to find the minimum button presses to reach the target state, where each button can be pressed 0 or 1 times (since pressing twice is the same as not pressing).

## Solution Approaches

### solution.py - BFS Approach (Recommended)
Uses breadth-first search to explore all possible states, guaranteeing the minimum number of presses.

**Time Complexity:** Exponential in number of lights, but works well for small problems (typically ≤10 lights).

### solution2.py - Gaussian Elimination Approach
Uses linear algebra over GF(2) to solve the system, but may not find the minimum weight solution.

**Note:** This approach finds a valid solution but not necessarily with minimum presses.

## Usage

```bash
# Test with example input
python3 solution.py input.md

# Run with actual input
python3 solution.py input.txt
```

## Example Results

For the example input:
- Machine 1: 2 presses
- Machine 2: 3 presses
- Machine 3: 2 presses
- Total: 7 presses

## Files

- `question.md` - Problem description
- `input.md` - Example input
- `input.txt` - Actual Advent of Code input (154 machines)
- `solution.py` - BFS solution (recommended)
- `solution2.py` - Gaussian elimination solution (not guaranteed to find minimum)

## Answers

**Part 1:** The fewest button presses required to correctly configure the indicator lights on all machines is **375**.

**Part 2:** The problem involves finding minimum button presses to reach exact joltage counter values. This is a complex optimization problem (solving A x = b with min sum x_i, x_i ≥ 0 integer). I've implemented BFS and Dijkstra algorithms in both Python and C++, which work on small examples but are too slow for the full problem due to large state space (10 counters with targets up to 286).

The example gives 33 total presses (10 + 12 + 11). A more efficient mathematical approach (linear algebra over rationals) would be needed for the full solution.

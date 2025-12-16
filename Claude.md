# Advent of Code 2025 - Repository Structure

This repository contains solutions for Advent of Code 2025 challenges.

## Repository Structure

Each day's challenge is organized in its own directory following this pattern:

```
Day[N]/
├── question.md         # Problem description (Part 1)
├── question2.md        # Problem description (Part 2, if different)
├── input.md           # Puzzle input data
├── solution.py        # Solution for Part 1
└── solution2.py       # Solution for Part 2
```

### Naming Conventions

Some directories include descriptive names:
- `Day 1 Secret Entrance/` - Day 1 challenge
- `Day 2 Gift Shop/` - Day 2 challenge
- `Day3/`, `Day4/`, `Day5/`, `Day6/` - Days 3-6 challenges

Alternate file names may appear in older days:
- `answer.py`, `answer1.py`, `answer2.py` - Alternative naming for solutions
- `soltuon2.py` - Typo variant of solution2.py

## File Descriptions

### question.md / question2.md
Contains the full problem statement from Advent of Code, including:
- Story/context
- Problem requirements
- Example input/output
- Expected behavior

### input.md
Your personalized puzzle input from Advent of Code. This data is unique to each user and is required to solve the challenge.

### solution.py / solution2.py
Python implementations that:
1. Parse the puzzle input
2. Implement the algorithm to solve the problem
3. Output the answer
4. Often include tests with the example data from the problem description

## Usage

To run a solution:

```bash
cd "Day[N]"
python solution.py
```

Most solutions will:
1. Test against the example input from the problem
2. Then attempt to solve using the actual input from `input.md`

## Development Workflow

1. Create new day directory: `mkdir "Day[N]"`
2. Add problem description to `question.md`
3. Add your puzzle input to `input.md`
4. Implement solution in `solution.py`
5. For Part 2, add `question2.md` and `solution2.py`

## Notes

- Solutions are written in Python
- Each solution is self-contained within its day's directory
- Input files use `.md` extension for easy viewing and editing
- Solutions typically include validation against example inputs before running on actual puzzle input

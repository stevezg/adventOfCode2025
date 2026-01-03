# solution.py
try:
    from ortools.linear_solver import pywraplp
    HAS_ORTOOLS = True
except ImportError:
    HAS_ORTOOLS = False
    print("Warning: OR-Tools not available, falling back to exploration method")

def solve_single_ilp(coeffs: list[tuple[int, ...]], goal: tuple[int, ...]) -> int:
    """Solve using Integer Linear Programming with OR-Tools."""
    if not HAS_ORTOOLS:
        # Fallback to the original exploration method
        return solve_single_exploration(coeffs, goal)

    n = len(goal)  # number of counters
    m = len(coeffs)  # number of buttons

    # Create solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        # Fallback to CBC if SCIP is not available
        solver = pywraplp.Solver.CreateSolver('CBC')
        if not solver:
            print("Warning: No ILP solver available, using exploration method")
            return solve_single_exploration(coeffs, goal)

    # Create variables: x[j] = number of times to press button j
    x = [solver.IntVar(0, solver.infinity(), f'x_{j}') for j in range(m)]

    # Add constraints: for each counter i, sum(button_j affects i) * x_j = goal[i]
    for i in range(n):
        constraint = solver.Constraint(goal[i], goal[i])
        for j in range(m):
            if i in coeffs[j]:  # if button j affects counter i
                constraint.SetCoefficient(x[j], 1)

    # Objective: minimize total presses
    objective = solver.Objective()
    for j in range(m):
        objective.SetCoefficient(x[j], 1)
    objective.SetMinimization()

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        return int(solver.Objective().Value())
    else:
        return -1  # No solution found

def solve_single_exploration(coeffs: list[tuple[int, ...]], goal: tuple[int, ...]) -> int:
    """Original exploration-based method as fallback."""
    from functools import cache
    from itertools import combinations, product

    def patterns(coeffs: list[tuple[int, ...]]) -> dict[tuple[int, ...], dict[tuple[int, ...], int]]:
        num_buttons = len(coeffs)
        num_variables = len(coeffs[0])
        out = {parity_pattern: {} for parity_pattern in product(range(2), repeat=num_variables)}
        for num_pressed_buttons in range(num_buttons + 1):
            for buttons in combinations(range(num_buttons), num_pressed_buttons):
                pattern = tuple(map(sum, zip((0,) * num_variables, *(coeffs[i] for i in buttons))))
                parity_pattern = tuple(i % 2 for i in pattern)
                if pattern not in out[parity_pattern]:
                    out[parity_pattern][pattern] = num_pressed_buttons
        return out

    pattern_costs = patterns(coeffs)
    @cache
    def solve_single_aux(goal: tuple[int, ...]) -> int:
        if all(i == 0 for i in goal):
            return 0
        answer = 1000000
        for pattern, pattern_cost in pattern_costs[tuple(i % 2 for i in goal)].items():
            if all(i <= j for i, j in zip(pattern, goal)):
                new_goal = tuple((j - i) // 2 for i, j in zip(pattern, goal))
                answer = min(answer, pattern_cost + 2 * solve_single_aux(new_goal))
        return answer
    return solve_single_aux(goal)

def solve_single(coeffs: list[tuple[int, ...]], goal: tuple[int, ...]) -> int:
    """Main solve function - uses ILP by default, falls back to exploration."""
    return solve_single_ilp(coeffs, goal)

def solve(raw: str):
    score = 0
    lines = raw.splitlines()
    for I, L in enumerate(lines, 1):
        _, *coeffs, goal = L.split()
        goal = tuple(int(i) for i in goal[1:-1].split(","))
        coeffs = [[int(i) for i in r[1:-1].split(",")] for r in coeffs]
        coeffs = [tuple(int(i in r) for i in range(len(goal))) for r in coeffs]
        subscore = solve_single(coeffs, goal)
        print(f'Line {I}/{len(lines)}: answer {subscore}')
        score += subscore
    print(score)
    return score  # Added return for testing

if __name__ == "__main__":
    with open("input.txt") as f:
        raw = f.read()
    solve(raw)
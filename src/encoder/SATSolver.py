from pysat.solvers import Glucose4


def solve(sat_problem):
    solver = Glucose4()
    for clause in sat_problem.clauses:
        solver.add_clause(clause)

    success = solver.solve()
    if success:
        sat_problem.result = solver.get_model()
    return success

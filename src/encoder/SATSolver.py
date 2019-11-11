from pysat.solvers import Glucose4
from src.encoder.SATProblem import SATProblem


def solve(sat_problem: SATProblem):
    solver = Glucose4()
    for clause in sat_problem.clauses:
        solver.add_clause(clause)

    success = solver.solve()
    if success:
        sat_problem.result = solver.get_model()

    sat_problem.success = success

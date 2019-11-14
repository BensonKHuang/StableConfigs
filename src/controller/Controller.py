from src.parser.Parser import parse_input_file
from src.encoder.SATProblem import SATProblem
import src.encoder.Encoder as Encoder
import time


def run(file_path):
    # parse the input to encode it into BindingSite/Monomer classes
    tbn_problem = parse_input_file(file_path)

    # encode problem to SAT solver compatible problem
    sat_problem = SATProblem()
    Encoder.encode_basic_clause(tbn_problem, sat_problem)

    # solve the problem (SAT solver)
    t0 = time.time()
    while sat_problem.success:
        Encoder.increment_min_representatives(tbn_problem, sat_problem)
        print("[ k =", sat_problem.min_reps, "]")
        sat_problem.solve()

    print(sat_problem.result)
    print(time.time() - t0)

    # decode the SAT solver output into Polymer classes
    pass

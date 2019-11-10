from src.parser.Parser import parse_input_file
from src.encoder.SATSolver import solve
from src.encoder.SATProblem import SATProblem

import src.encoder.Encoder as Encoder

if __name__ == '__main__':
    # parse the input to encode it into BindingSite/Monomer classes
    tbn_problem = parse_input_file("../input/basic.txt")

    # encode problem to SAT solver compatible problem
    sat_problem = SATProblem()

    Encoder.encode_basic_clause(tbn_problem, sat_problem)


    # solve the problem (SAT solver)
    pass

    # decode the SAT solver output into Polymer classes
    pass

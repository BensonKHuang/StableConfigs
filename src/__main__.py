from src.parser.Parser import parse_input_file

if __name__ == '__main__':
    # parse the input to encode it into BindingSite/Monomer classes
    tbn_problem = parse_input_file("input/basic.txt")

    # encode problem to SAT solver compatible problem
    pass

    # solve the problem (SAT solver)
    pass

    # decode the SAT solver output into Polymer classes
    pass

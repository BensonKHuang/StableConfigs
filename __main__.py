from Parser import parse_input_file
from BindingSite import BindingSite

if __name__ == '__main__':
    # parse the input to encode it into BindingSite/Monomer classes
    parse_input_file("input/basic.txt")
    limiting_site = BindingSite.get_limiting_site()

    # encode problem to SAT solver compatible problem
    pass

    # solve the problem (SAT solver)
    pass

    # decode the SAT solver output into Polymer classes
    pass

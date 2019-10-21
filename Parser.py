# Parser library
from BindingSite import BindingSite
from Monomer import Monomer
from Problem import Problem


def parse_monomer(problem_obj, str_line):
    all_sites = []
    tokens = str_line.replace("\n", "").split(' ')

    for token in tokens:
        all_sites.append(BindingSite(problem_obj, token))

    return Monomer(problem_obj, all_sites)


def parse_input_file(input_file):
    new_problem = Problem()
    open_file = open(input_file, 'rt')

    while True:
        try:
            next_line = open_file.next()
            parse_monomer(new_problem, next_line)
        except StopIteration:
            break

    return new_problem

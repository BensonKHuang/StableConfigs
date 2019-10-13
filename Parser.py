# Parser library
from BindingSite import BindingSite
from Monomer import Monomer


def parse_monomer(str_line):
    all_sites = []
    tokens = str_line.replace("\n", "").split(' ')

    for token in tokens:
        all_sites.append(BindingSite(token))

    return Monomer(all_sites)


def parse_input_file(input_file):
    open_file = open(input_file, 'rt')

    while True:
        try:
            next_line = open_file.next()
            parse_monomer(next_line)
        except StopIteration:
            break

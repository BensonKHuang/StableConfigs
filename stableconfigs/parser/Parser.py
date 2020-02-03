# Parser library
from stableconfigs.common.Instruction import Instruction
from stableconfigs.common.BindingSite import BindingSite
from stableconfigs.common.Monomer import Monomer
from stableconfigs.common.TBNProblem import TBNProblem
from stableconfigs.common.SiteList import SiteList


def parse_monomer(tbn_problem, str_line):
    all_sites = []
    tokens = str_line.replace("\n", "").split(' ')

    # Check for duplicate names
    monomer_name = None
    for token in tokens:
        if token[0] == ":":
            assert (monomer_names is None), "Monomer given multiple names."  # TODO Add error handling.
            monomer_names = token[1:].strip()
        else:
            site = BindingSite(tbn_problem, token)
            all_sites.append(site)

            # Create a new SiteMap for a specific type
            if site.name not in tbn_problem.site_name_to_sitelist_map:
                tbn_problem.site_name_to_sitelist_map[site.name] = SiteList(site.name)

            tbn_problem.site_name_to_sitelist_map[site.name].add(site)
    new_monomer = Monomer(tbn_problem, all_sites)

    # If monomer name exists, add it to monomer name map in the tbn problem
    if monomer_name is not None:
        tbn_problem.assign_name(monomer_name, new_monomer)
    return new_monomer


def parse_instruction(tbn_problem, str_line):
    i_type = None
    monomer_names = list()
    tokens = str_line.replace("\n", "").split(' ')

    for ind in range(len(tokens)):
        token = tokens[ind]
        if ind == 0:
            i_type = token
        else:
            monomer_names.append(token)

    return Instruction(tbn_problem, i_type, monomer_names)


def parse_input_file(input_file, instr_file):
    tbn_problem = TBNProblem()
    
    # parse input
    open_file = open(input_file, 'rt')
    next_line = open_file.readline()
    while next_line:
        parse_monomer(tbn_problem, next_line)
        next_line = open_file.readline()
    open_file.close()

    # parse instr
    if instr_file is not None:
        open_file = open(instr_file, 'rt')
        next_line = open_file.readline()
        while next_line:
            parse_instruction(tbn_problem, next_line)     
            next_line = open_file.readline()
        open_file.close()

    return tbn_problem

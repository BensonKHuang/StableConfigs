# Parser library
from stableconfigs.common.BindingSite import BindingSite
from stableconfigs.common.Monomer import Monomer
from stableconfigs.common.TBNProblem import TBNProblem
from stableconfigs.common.SiteList import SiteList


def parse_monomer(tbn_problem, str_line):
    all_sites = []
    tokens = str_line.replace("\n", "").split(' ')

    monomer_names = None
    for token in tokens:
        if token[0] == "$":
            assert monomer_names == None, "Monomer given multiple names." # TODO Add error handling.
            monomer_names = token[1:]
        else:
            site = BindingSite(tbn_problem, token)
            all_sites.append(site)

            # Create a new SiteMap for a specific type
            if site.name not in tbn_problem.site_name_to_sitelist_map:
                tbn_problem.site_name_to_sitelist_map[site.name] = SiteList(site.name)

            tbn_problem.site_name_to_sitelist_map[site.name].add(site)

    new_Monomer = Monomer(tbn_problem, all_sites)
    if monomer_names is not None:
        new_Monomer.assign_name(monomer_names)
    return new_Monomer


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
            
            next_line = open_file.readline()
        open_file.close()

    return tbn_problem

# Parser library
from stableconfigs.common.Instruction import Instruction, INSTR
from stableconfigs.common.BindingSite import BindingSite
from stableconfigs.common.Monomer import Monomer
from stableconfigs.common.TBNProblem import TBNProblem
from stableconfigs.common.SiteList import SiteList


def parse_monomer(tbn_problem: TBNProblem, str_line: str):
    all_sites = []
    tokens = str_line.strip().split(' ')

    monomer_name = None
    for token in tokens:
        if token[0] == ">":
            assert (monomer_name is None), "Monomer given multiple names."  # TODO Add error handling.
            monomer_name = token[1:].strip()
        else:
            find_site_name = token.find(":")
            site_name = None
            if find_site_name != -1:
                site_name = token[(find_site_name + 1):]
                token = token[:find_site_name]
                # TODO: global error checking
                assert(len(site_name) > 0 and len(token) > 0, "Invalid Binding Site name.")

            site = BindingSite(tbn_problem, token)
            all_sites.append(site)

            if site_name is not None:
                # TODO: Check for duplicate BindingSite names.
                assert(site_name not in tbn_problem.bindingsite_name_map, "Duplicate BindingSite name.")
                tbn_problem.assign_bindingsite_name(site, site_name)

            # Create a new SiteMap for a specific type
            if site.name not in tbn_problem.site_name_to_sitelist_map:
                tbn_problem.site_name_to_sitelist_map[site.name] = SiteList(site.name)

            tbn_problem.site_name_to_sitelist_map[site.name].add(site)
    new_monomer = Monomer(tbn_problem, all_sites)

    # If monomer name exists, add it to monomer name map in the tbn problem
    if monomer_name is not None:
        # TODO: Check for duplicate Monomer names
        assert(monomer_name not in tbn_problem.monomer_name_map, "Duplicate monomer name.")
        tbn_problem.assign_monomer_name(new_monomer, monomer_name)
    return new_monomer


def parse_instruction(tbn_problem, str_line):
    i_type = None
    monomer_names = list()
    tokens = str_line.replace("\n", "").split(' ')  # TODO: Fix bug where you can have spaces in name

    for ind in range(len(tokens)):
        token = tokens[ind]
        if ind == 0:
            i_type = token
        else:
            monomer_names.append(token)
    if i_type == INSTR.GEN:
        if len(tokens) > 1:
            get_num = None
            try:
                get_num = int(tokens[1])
            except ValueError:
                get_num = None
            if get_num is not None:
                tbn_problem.gen_count = get_num
            # TODO: Throw exception on bad number.
    else:
        Instruction(tbn_problem, i_type, monomer_names)


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

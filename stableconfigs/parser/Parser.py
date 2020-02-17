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
            if site.type not in tbn_problem.site_type_to_sitelist_map:
                tbn_problem.site_type_to_sitelist_map[site.type] = SiteList(site.type)

            tbn_problem.site_type_to_sitelist_map[site.type].add(site)
    new_monomer = Monomer(tbn_problem, all_sites)

    # If monomer name exists, add it to monomer name map in the tbn problem
    if monomer_name is not None:
        # TODO: Check for duplicate Monomer names
        assert(monomer_name not in tbn_problem.monomer_name_map, "Duplicate monomer name.")
        tbn_problem.assign_monomer_name(new_monomer, monomer_name)
    return new_monomer


def parse_instruction(tbn_problem, str_line):
    tokens = str_line.replace("\n", "").split(' ')  # TODO: Fix bug where you can have spaces in name

    i_type = None
    arguments = list()  # For the most part, these are monomer names.

    for ind in range(len(tokens)):
        token = tokens[ind]

        find_hash = token.find("#")
        if find_hash != -1:
            if find_hash == 0:  # if the '#' is found in the beginning of the token, the entire token is a comment
                break
            else:
                token = token[:find_hash]

        if ind == 0:
            i_type = token
        else:
            arguments.append(token)

        if find_hash != -1:
            break

    if i_type in Instruction.instr_set:
        if INSTR.arg_count[i_type] != -1 and len(arguments) != INSTR.arg_count[i_type]:
            pass
            # TODO: Throw invalid instr count error.
        else:
            if i_type == INSTR.GEN:
                get_num = None
                try:
                    get_num = int(arguments[0])
                except ValueError:
                    get_num = None
                if get_num is not None:
                    tbn_problem.gen_count = get_num
                # TODO: Throw exception on non-positive numbers.
            else:
                Instruction(tbn_problem, i_type, arguments)


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

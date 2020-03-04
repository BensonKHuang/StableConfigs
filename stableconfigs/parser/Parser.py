# Parser library
from stableconfigs.common.Instruction import Instruction, INSTR
from stableconfigs.common.BindingSite import BindingSite
from stableconfigs.common.Monomer import Monomer
from stableconfigs.common.TBNProblem import TBNProblem
from stableconfigs.common.SiteList import SiteList
from stableconfigs.common.CustomExceptions import *

def parse_monomer(tbn_problem: TBNProblem, str_line: str):
    all_sites = []
    str_line = str_line.strip()
    tokens = str_line.split(' ')

    monomer_name = None
    for token in tokens:
        if token[0] == ">":
            if monomer_name is not None:
                raise MonomerMultipleNames(str_line)
            monomer_name = token[1:].strip()
        else:
            find_site_name = token.find(":")
            site_name = None
            if find_site_name != -1:
                site_name = token[(find_site_name + 1):]
                token = token[:find_site_name]
                if len(site_name) == 0 or len(token) == 0:
                    raise InvalidBindingSiteName(str_line)

            site = BindingSite(tbn_problem, token)
            all_sites.append(site)

            if site_name is not None:
                if site_name in tbn_problem.bindingsite_name_map:
                    raise DuplicateBindingSiteName(str_line)
                tbn_problem.assign_bindingsite_name(site, site_name)

            # Create a new SiteMap for a specific type
            if site.type not in tbn_problem.site_type_to_sitelist_map:
                tbn_problem.site_type_to_sitelist_map[site.type] = SiteList(site.type)

            tbn_problem.site_type_to_sitelist_map[site.type].add(site)
    new_monomer = Monomer(tbn_problem, all_sites)

    # If monomer name exists, add it to monomer name map in the tbn problem
    if monomer_name is not None:
        if monomer_name in tbn_problem.monomer_name_map:
            raise DuplicateMonomerName(str_line)
        tbn_problem.assign_monomer_name(new_monomer, monomer_name)


def parse_instruction(tbn_problem, str_line):
    str_line = str_line.strip()
    tokens = str_line.split(' ')

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
            raise InstructionArgumentCount(str_line, i_type, INSTR.arg_count[i_type], len(arguments))
        else:
            if i_type in Instruction.binding_instr:
                for arg in arguments:
                    if arg not in tbn_problem.bindingsite_name_map:
                        raise NonexistentBindingSite(str_line, arg)
            else:
                for arg in arguments:
                    if arg not in tbn_problem.monomer_name_map:
                        raise NonexistentMonomer(str_line, arg)
            Instruction(tbn_problem, i_type, arguments)
    else:
        raise InvalidInstruction(str_line, i_type)


def parse_input_lines(tbn_lines, instr_lines):
    tbn_problem = TBNProblem()
    
    # parse input
    for tbn_line in tbn_lines:
        parse_monomer(tbn_problem, tbn_line)

    # parse instr
    for instr_line in instr_lines:
        parse_instruction(tbn_problem, instr_line)
        
    return tbn_problem
    
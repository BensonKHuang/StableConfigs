# Parser library
from stableconfigs.common.Constraint import Constraint, CONSTR
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
        
        # Ignore empty lines
        if token is "":
            break

        find_hash = token.find("#")
        if find_hash != -1:
            if find_hash == 0:  # if the hash was the first character, the entire line is a comment
                break
            else:
                token = token[:find_hash]

        if token[0] == ">":
            if monomer_name is not None:
                raise MonomerMultipleNamesException(str_line)
            monomer_name = token[1:].strip()
            if len(monomer_name) == 0 or monomer_name == '':
                raise InvalidMonomerNameException(str_line)
        else:
            find_site_name = token.find(":")
            site_name = None
            if find_site_name != -1:
                site_name = token[(find_site_name + 1):]
                token = token[:find_site_name]
                if len(site_name) == 0 or len(token) == 0:
                    raise InvalidBindingSiteNameException(str_line)

            site = BindingSite(tbn_problem, token)
            all_sites.append(site)

            if site_name is not None:
                if site_name in tbn_problem.bindingsite_name_map:
                    raise DuplicateBindingSiteNameException(str_line)
                tbn_problem.assign_bindingsite_name(site, site_name)

            # Create a new SiteMap for a specific type
            if site.type not in tbn_problem.site_type_to_sitelist_map:
                tbn_problem.site_type_to_sitelist_map[site.type] = SiteList(site.type)

            tbn_problem.site_type_to_sitelist_map[site.type].add(site)

        if find_hash != -1:
            break
    
    if len(all_sites) == 0:
        return
        
    new_monomer = Monomer(tbn_problem, all_sites)

    # If monomer name exists, add it to monomer name map in the tbn problem
    if monomer_name is not None:
        if monomer_name in tbn_problem.monomer_name_map:
            raise DuplicateMonomerNameException(str_line)
        tbn_problem.assign_monomer_name(new_monomer, monomer_name)


def parse_constraint(tbn_problem: TBNProblem, str_line: str):
    str_line = str_line.strip()
    tokens = str_line.split(' ')

    c_type = None
    arguments = list()  # For the most part, these are monomer names.

    for ind in range(len(tokens)):
        token = tokens[ind]

        find_hash = token.find("#")
        if find_hash != -1:
            if find_hash == 0:
                break
            else:
                token = token[:find_hash]

        if ind == 0:
            c_type = token
        else:
            arguments.append(token)

        if find_hash != -1:
            break

    # If constraint file is blank/Only a comment, then just ignore constraint.
    if c_type is None:
        return
    
    if c_type in Constraint.constr_set:
        if CONSTR.arg_count[c_type] != -1 and len(arguments) != CONSTR.arg_count[c_type]:
            raise ConstraintArgumentCountException(
                str_line, c_type, CONSTR.arg_count[c_type], len(arguments))
        else:
            if c_type in Constraint.binding_constr:
                for arg in arguments:
                    if arg not in tbn_problem.bindingsite_name_map:
                        raise NonexistentBindingSiteException(str_line, arg)
            else:
                for arg in arguments:
                    if arg not in tbn_problem.monomer_name_map:
                        raise NonexistentMonomerException(str_line, arg)
            Constraint(tbn_problem, c_type, arguments)
    else:
        raise InvalidConstraintException(str_line, c_type)


def parse_input_lines(tbn_lines, constr_lines):
    tbn_problem = TBNProblem()
    
    # parse input
    for tbn_line in tbn_lines:
        parse_monomer(tbn_problem, tbn_line)
    
    if len(tbn_problem.all_monomers) == 0:
        raise EmptyProblemException()

    # parse constr
    for constr_line in constr_lines:
        parse_constraint(tbn_problem, constr_line)
        
    return tbn_problem
    

# Parser library
from stableconfigs.common.BindingSite import BindingSite
from stableconfigs.common.Monomer import Monomer
from stableconfigs.common.TBNProblem import TBNProblem
from stableconfigs.common.SiteList import SiteList


def parse_monomer(tbn_problem, str_line):
    all_sites = []
    tokens = str_line.replace("\n", "").split(' ')

    for token in tokens:
        site = BindingSite(tbn_problem, token)
        all_sites.append(site)

        # Create a new SiteMap for a specific type
        if site.name not in tbn_problem.site_name_to_sitelist_map:
            tbn_problem.site_name_to_sitelist_map[site.name] = SiteList(site.name)

        tbn_problem.site_name_to_sitelist_map[site.name].add(site)

    return Monomer(tbn_problem, all_sites)


def parse_input_file(input_file):
    tbn_problem = TBNProblem()
    open_file = open(input_file, 'rt')
    next_line = open_file.readline()
    while next_line:
        parse_monomer(tbn_problem, next_line)
        next_line = open_file.readline()

    open_file.close()
    return tbn_problem

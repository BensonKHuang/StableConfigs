# TBNProblem Class


class TBNProblem:
    # CONSTRUCTOR

    def __init__(self):
        self.site_count = 0
        self.monomer_count = 0

        # site name to objects map
        self.site_name_to_sitelist_map = dict()

        self.all_monomers = list()

        self.instr = list()

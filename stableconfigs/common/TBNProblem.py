# TBNProblem Class


class TBNProblem:
    # CONSTRUCTOR

    def __init__(self):
        self.site_count = 0
        self.monomer_count = 0

        # site name to objects map
        self.site_name_to_sitelist_map = dict()

        self.all_monomers = list()
        self.monomer_name_map = dict()

        self.instructions = list()

    def assign_name(self, monomer_name, monomer):
        assert(monomer_name is not None) #TODO: Error handling
        monomer.name = monomer_name
        self.monomer_name_map[monomer_name] = monomer

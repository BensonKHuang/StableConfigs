# Monomer Class


class Monomer:
    monomer_name_map = dict()
   
    # CONSTRUCTOR
    def __init__(self, tbn_problem, binding_sites):  # binding_sites = [BindingSite, BindingSite, ...]
        # increment unique_id
        tbn_problem.monomer_count = tbn_problem.monomer_count + 1

        # parent all sites
        for BindingSite in binding_sites:
            BindingSite.ParentMonomer = self

        # constructor
        self.name = None
        self.id = tbn_problem.monomer_count
        self.BindingSites = binding_sites

        # add monomer to lis
        tbn_problem.all_monomers.append(self)

    def assign_name(monomer_name):
        if self.name is not None:
            monomer_id_map[self.name] = None
        self.name = monomer_name
        if monomer_name is not None:
            monomer_id_map[monomer_name] = self

    def get_max(self, other):
        return self if self.id > other.id else other

    @staticmethod
    def monomer_from_name(monomer_name):
        return monomer_id_map[monomer_name]

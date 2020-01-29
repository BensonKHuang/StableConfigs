# Monomer Class


class Monomer:
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

    def get_max(self, other):
        return self if self.id > other.id else other

    @staticmethod
    def monomer_from_name(monomer_name):
        return Monomer.monomer_id_map[monomer_name]

    def __str__(self):
        monomer_name = ("\t" + self.name) if self.name is not None else ""
        return (str(list(map(lambda x: (x.name + "*") if x.IsComplement else x.name, self.BindingSites))) + monomer_name) 
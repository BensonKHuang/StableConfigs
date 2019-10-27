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
        self.id = tbn_problem.monomer_count
        self.BindingSites = binding_sites

        # add monomer to lis
        tbn_problem.all_monomers.append(self)

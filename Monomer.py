# Monomer Class


class Monomer:
    # CONSTRUCTOR

    def __init__(self, problem_obj, binding_sites):  # binding_sites = [BindingSite, BindingSite, ...]
        # increment unique_id
        problem_obj.monomer_count = problem_obj.monomer_count + 1

        # parent all sites
        for BindingSite in binding_sites:
            BindingSite.ParentMonomer = self

        # constructor
        self.id = problem_obj.monomer_count
        self.BindingSites = binding_sites

        # add monomer to lis
        problem_obj.all_monomers.append(self)

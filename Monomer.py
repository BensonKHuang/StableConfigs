# Monomer Class


class Monomer:
    unique_id = 0
    all_Monomers = []

    # CONSTRUCTOR

    def __init__(self, binding_sites):  # binding_sites = [BindingSite, BindingSite, ...]
        # increment unique_id
        Monomer.unique_id = Monomer.unique_id + 1

        # parent all sites
        for BindingSite in binding_sites:
            BindingSite.ParentMonomer = self

        # constructor
        self.id = Monomer.unique_id
        self.BindingSites = binding_sites

        # append new Monomer to all_Monomers
        Monomer.all_Monomers.append(self)

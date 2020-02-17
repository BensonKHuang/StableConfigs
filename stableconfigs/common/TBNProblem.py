# TBNProblem Class


class TBNProblem:
    # CONSTRUCTOR

    def __init__(self):
        self.site_count = 0
        self.monomer_count = 0

        # site name to objects map
        self.site_type_to_sitelist_map = dict()

        self.all_monomers = list()
        self.monomer_name_map = dict()
        self.bindingsite_name_map = dict()

        self.gen_count = 1

        self.instructions = list()

    def assign_monomer_name(self, monomer, monomer_name):
        monomer.name = monomer_name
        self.monomer_name_map[monomer_name] = monomer

    def assign_bindingsite_name(self, bindingsite, bindingsite_name):
        bindingsite.name = bindingsite_name
        self.bindingsite_name_map[bindingsite_name] = bindingsite

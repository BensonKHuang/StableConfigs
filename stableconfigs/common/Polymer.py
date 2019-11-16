# Polymer Class


class Polymer:
    # CONSTRUCTOR

    def __init__(self):
        self.monomer_list = list()
    
    def add_monomer(self, monomer):
        self.monomer_list.append(monomer)
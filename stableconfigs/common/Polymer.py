# Polymer Class


class Polymer:
    # CONSTRUCTOR

    def __init__(self):
        self.monomer_list = list()
    
    def add_monomer(self, monomer):
        self.monomer_list.append(monomer)

    def to_json_format(self):
        cur_polymer = []
        for monomer in self.monomer_list:
            cur_polymer.append(monomer.to_json_format())
        return cur_polymer

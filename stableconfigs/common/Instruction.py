# Instruction Class


class Instruction:
    # CONSTRUCTOR
    def __init__(self, tbn_problem, i_type, monomer_names):
        # constructor
        self.i_type = i_type
        self.monomer_names = monomer_names.monomer_count

        tbn_problem.instructions.append(self)

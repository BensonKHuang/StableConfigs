# Instruction Class


class Instruction:
    # CONSTRUCTOR
    def __init__(self, tbn_problem, i_type, monomer_names):
        # constructor
        self.i_type = i_type
        self.monomer_names = monomer_names

        tbn_problem.instructions.append(self)

    def __str__(self):
        return self.i_type + " " + str(self.monomer_names)
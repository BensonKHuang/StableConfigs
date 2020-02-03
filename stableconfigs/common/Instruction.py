# Instruction Class


class Instruction:

    TOGETHER_INSTR = "TOGETHER"
    FREE_INSTR = "FREE"
    IGNORE_INSTR = "IGNORE"

    # CONSTRUCTOR
    def __init__(self, tbn_problem, i_type, monomer_names):
        # constructor
        if i_type == self.TOGETHER_INSTR or i_type == self.FREE_INSTR:
            self.i_type = i_type
        else:
            # TODO: Throw error for invalid instruction
            self.i_type = self.IGNORE_INSTR
            
        self.monomer_names = monomer_names

        tbn_problem.instructions.append(self)

    def __str__(self):
        return self.i_type + " " + str(self.monomer_names)
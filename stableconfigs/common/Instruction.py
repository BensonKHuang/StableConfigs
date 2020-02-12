# Instruction Class

class INSTR:
    GEN = "GEN"
    TOGETHER = "TOGETHER"
    NOTTOGETHER = "NOTTOGETHER"
    FREE = "FREE"
    NOTFREE = "NOTFREE"
    PAIRED = "PAIRED"
    NOTPAIRED = "NOTPAIRED"
    ANYPAIRED = "ANYPAIRED"
    NOTANYPAIRED = "NOTANYPAIRED"

class Instruction:

    instr_set = set([
        INSTR.GEN,
        INSTR.TOGETHER,
        INSTR.NOTTOGETHER,
        INSTR.FREE,
        INSTR.NOTFREE,
        INSTR.PAIRED,
        INSTR.NOTPAIRED,
        INSTR.ANYPAIRED,
        INSTR.NOTANYPAIRED,
    ])

    # CONSTRUCTOR
    def __init__(self, tbn_problem, i_type, monomer_names):
        # constructor
        if i_type in self.instr_set:
            self.i_type = i_type
        else:
            # TODO: Throw error for invalid instruction
            pass
            
        # TODO: Error handling for duplicate monomer names in same list
        self.monomer_names = monomer_names

        tbn_problem.instructions.append(self)

    def __str__(self):
        return self.i_type + " " + str(self.monomer_names)
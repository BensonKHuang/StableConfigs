# Instruction Class


class INSTR:
    arg_count = dict()

    TOGETHER = "TOGETHER";         arg_count[TOGETHER] = -1
    NOTTOGETHER = "NOTTOGETHER";   arg_count[NOTTOGETHER] = 2
    FREE = "FREE";                 arg_count[FREE] = 1
    NOTFREE = "NOTFREE";           arg_count[NOTFREE] = 1
    PAIRED = "PAIRED";             arg_count[PAIRED] = 2
    NOTPAIRED = "NOTPAIRED";       arg_count[NOTPAIRED] = 2
    ANYPAIRED = "ANYPAIRED";       arg_count[ANYPAIRED] = 1
    NOTANYPAIRED = "NOTANYPAIRED"; arg_count[NOTANYPAIRED] = 1


class Instruction:
    instr_set = {
        INSTR.TOGETHER,
        INSTR.NOTTOGETHER,
        INSTR.FREE,
        INSTR.NOTFREE,
        INSTR.PAIRED,
        INSTR.NOTPAIRED,
        INSTR.ANYPAIRED,
        INSTR.NOTANYPAIRED
    }

    # CONSTRUCTOR
    def __init__(self, tbn_problem, i_type, arguments):
        # constructor
        if i_type in self.instr_set:
            self.i_type = i_type
        else:
            # TODO: Throw error for invalid instruction
            pass
            
        # TODO: Error handling for duplicate monomer names in same list
        self.arguments = arguments

        tbn_problem.instructions.append(self)

    def __str__(self):
        return self.i_type + " " + str(self.arguments)

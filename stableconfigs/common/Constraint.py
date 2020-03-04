# Constraint Class


class CONSTR:
    arg_count = dict()

    TOGETHER = "TOGETHER";         arg_count[TOGETHER] = -1
    NOTTOGETHER = "NOTTOGETHER";   arg_count[NOTTOGETHER] = 2
    FREE = "FREE";                 arg_count[FREE] = 1
    NOTFREE = "NOTFREE";           arg_count[NOTFREE] = 1

    PAIRED = "PAIRED";             arg_count[PAIRED] = 2
    NOTPAIRED = "NOTPAIRED";       arg_count[NOTPAIRED] = 2
    ANYPAIRED = "ANYPAIRED";       arg_count[ANYPAIRED] = 1
    NOTANYPAIRED = "NOTANYPAIRED"; arg_count[NOTANYPAIRED] = 1


class Constraint:
    constr_set = {
        CONSTR.TOGETHER,
        CONSTR.NOTTOGETHER,
        CONSTR.FREE,
        CONSTR.NOTFREE,
        CONSTR.PAIRED,
        CONSTR.NOTPAIRED,
        CONSTR.ANYPAIRED,
        CONSTR.NOTANYPAIRED
    }

    binding_constr = {
        CONSTR.PAIRED,
        CONSTR.NOTPAIRED,
        CONSTR.ANYPAIRED,
        CONSTR.NOTANYPAIRED
    }

    # CONSTRUCTOR
    def __init__(self, tbn_problem, c_type, arguments):
        # constructor
        if c_type in self.constr_set:
            self.c_type = c_type
        else:
            # TODO: Throw error for invalid constraints
            pass
            
        self.arguments = arguments

        tbn_problem.constraints.append(self)

    def __str__(self):
        return self.c_type + " " + str(self.arguments)

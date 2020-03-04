# Custom Exceptions


class MonomerMultipleNames(Exception):
    def __init__(self, str_line):
        self.str_line = str_line
    def __str__(self):
        return "Monomer given multiple names. '" + self.str_line + "'"

class InvalidBindingSiteName(Exception):
    def __init__(self, str_line):
        self.str_line = str_line
    def __str__(self):
        return "Invalid BindingSite name. '" + self.str_line + "'"

class DuplicateBindingSiteName(Exception):
    def __init__(self, str_line):
        self.str_line = str_line
    def __str__(self):
        return "Duplicate BindingSite name. '" + self.str_line + "'"

class DuplicateMonomerName(Exception):
    def __init__(self, str_line):
        self.str_line = str_line
    def __str__(self):
        return "Duplicate Monomer name. '" + self.str_line + "'"

class InstructionArgumentCount(Exception):
    def __init__(self, str_line, i_type, expected_count, actual_count):
        self.str_line = str_line
        self.i_type = i_type
        self.expected_count = expected_count
        self.actual_count = actual_count
    def __str__(self):
        return "Instruction '" + self.i_type + "' takes " + str(self.expected_count) + " arguments, got " \
                + str(self.actual_count) + ". '" + self.str_line + "'"

class NonexistentBindingSite(Exception):
    def __init__(self, str_line, bad_name):
        self.str_line = str_line
        self.bad_name = bad_name
    def __str__(self):
        return "BindingSite '" + self.bad_name + "' does not exist. '" + self.str_line + "'"

class NonexistentMonomer(Exception):
    def __init__(self, str_line, bad_name):
        self.str_line = str_line
        self.bad_name = bad_name
    def __str__(self):
        return "Monomer '" + self.bad_name + "' does not exist. '" + self.str_line + "'"

class InvalidInstruction(Exception):
    def __init__(self, str_line, bad_instr):
        self.str_line = str_line
        self.bad_instr = bad_instr
    def __str__(self):
        return "Invalid Instruction '" + self.bad_name + "'. '" + self.str_line + "'"

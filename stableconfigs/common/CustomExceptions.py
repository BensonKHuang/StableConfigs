# Custom Exceptions


class EmptyProblemException(Exception):
    def __str__(self):
        return "Input contains no monomers."

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


# Exceptions for Executing Instructions

class TogetherConstraintException(Exception):
    def __init__(self, instruction, mon1, mon2):
        self.instruction = instruction
        self.mon1 = mon1
        self.mon2 = mon2
    def __str__(self):
        return "Monomer [" + self.mon1.name + "] and Monomer [" + self.mon2.name + "] cannot be together in any valid configuration."

class NotFreeConstraintException(Exception):
    def __init__(self, instruction, mon):
        self.instruction = instruction
        self.mon = mon
    def __str__(self):
        return "Monomer [" + self.mon.name +"] cannot be together with any other Monomer in any valid configuration."

class PairedConstraintException(Exception):
    def __init__(self, instruction, bsite1, bsite2):
        self.instruction = instruction
        self.bsite1 = bsite1
        self.bsite2 = bsite2
    def __str__(self):
        return "Binding Site [" + self.bsite1.name + "] and Binding Site [" + self.bsite2.name + "] do not have complementary Binding Sites."

class AnyPairedConstraintException(Exception):
    def __init__(self, instruction, bsite):
        self.instruction = instruction
        self.bsite = bsite
    def __str__(self):
        return "Binding Site [" + self.bsite.name + "] does not have any complementary binding sites in the system."
    
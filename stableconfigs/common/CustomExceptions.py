# Custom Exceptions

class TBNException(Exception):
    def __str__(self):
        return ""


class EmptyProblemException(TBNException):
    def __str__(self):
        return "Input contains no monomers."


class MonomerMultipleNames(TBNException):
    def __init__(self, str_line):
        self.str_line = str_line
    def __str__(self):
        return "Monomer given multiple names. '" + self.str_line + "'"


class InvalidBindingSiteName(TBNException):
    def __init__(self, str_line):
        self.str_line = str_line
    def __str__(self):
        return "Invalid BindingSite name. '" + self.str_line + "'"


class DuplicateBindingSiteName(TBNException):
    def __init__(self, str_line):
        self.str_line = str_line
    def __str__(self):
        return "Duplicate BindingSite name. '" + self.str_line + "'"


class DuplicateMonomerName(TBNException):
    def __init__(self, str_line):
        self.str_line = str_line
    def __str__(self):
        return "Duplicate Monomer name. '" + self.str_line + "'"


class ConstraintArgumentCount(TBNException):
    def __init__(self, str_line, c_type, expected_count, actual_count):
        self.str_line = str_line
        self.c_type = c_type
        self.expected_count = expected_count
        self.actual_count = actual_count
    def __str__(self):
        return "Constraint '" + self.c_type + "' takes " + str(self.expected_count) + " arguments, got " \
                + str(self.actual_count) + ". '" + self.str_line + "'"


class NonexistentBindingSite(TBNException):
    def __init__(self, str_line, bad_name):
        self.str_line = str_line
        self.bad_name = bad_name
    def __str__(self):
        return "BindingSite '" + self.bad_name + "' does not exist. '" + self.str_line + "'"


class NonexistentMonomer(TBNException):
    def __init__(self, str_line, bad_name):
        self.str_line = str_line
        self.bad_name = bad_name
    def __str__(self):
        return "Monomer '" + self.bad_name + "' does not exist. '" + self.str_line + "'"


class InvalidConstraint(TBNException):
    def __init__(self, str_line, bad_constr):
        self.str_line = str_line
        self.bad_constr = bad_constr
    def __str__(self):
        return "Invalid Constraint '" + self.bad_name + "'. '" + self.str_line + "'"


# Exceptions for Executing Constraints

class TogetherConstraintException(TBNException):
    def __init__(self, constraint, mon1, mon2):
        self.constraint = constraint
        self.mon1 = mon1
        self.mon2 = mon2
    def __str__(self):
        return "Monomer [" + self.mon1.name + "] and Monomer [" + self.mon2.name + "] cannot be together in any valid configuration."


class NotFreeConstraintException(TBNException):
    def __init__(self, constraint, mon):
        self.constraint = constraint
        self.mon = mon
    def __str__(self):
        return "Monomer [" + self.mon.name +"] cannot be together with any other Monomer in any valid configuration."


class PairedConstraintException(TBNException):
    def __init__(self, constraint, bsite1, bsite2):
        self.constraint = constraint
        self.bsite1 = bsite1
        self.bsite2 = bsite2
    def __str__(self):
        return "Binding Site [" + self.bsite1.name + "] and Binding Site [" + self.bsite2.name + "] are not complementary."


class AnyPairedConstraintException(TBNException):
    def __init__(self, constraint, bsite):
        self.constraint = constraint
        self.bsite = bsite
    def __str__(self):
        return "Binding Site [" + self.bsite.name + "] does not have any complementary binding sites in the system."
    

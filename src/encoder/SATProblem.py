# SATProblem Class


class SATProblem:
    # CONSTRUCTOR

    def __init__(self):
        self.clauses = list()
        self.result = list()

    def add_clause(self, clause):
        self.clauses.append(clause)

# SATProblem Class


class SATProblem:
    # CONSTRUCTOR

    def __init__(self):
        self.clauses = list()
        self.result = list()
        #string of boolean representation to object
        self.pair_to_id = set()
        self.id_to_pair = dict()
        self.unique_id = 0



    def add_clause(self, clause):
        self.clauses.append(clause)

    def get_unique_id(self):
    	unique_id = unique_id + 1
    	return unique_id

   	def get_pair_id(site1, site2):
   		pairObj = Pair(site1, site2)
   		if pairObj in pair_to_id.keys():
   			return pair_to_id[pairObj]
   		else:
   			new_id = self.get_unique_id()
   			pair_to_id[pairObj] = new_id
   			id_to_pair[new_id] = pairObj
   			return new_id


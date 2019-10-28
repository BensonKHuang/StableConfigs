# SATProblem Class
from src.encoder.boolean.Pair import Pair


class SATProblem:
    # CONSTRUCTOR
	def __init__(self):
		self.clauses = list()
		self.result = list()
		# string of boolean representation to object
		self.pair_to_id = dict()
		self.id_to_pair = dict()
		self.unique_id = 0

	def add_clause(self, clause):
		self.clauses.append(clause)

	def get_unique_id():
		self.unique_id += 1
		return self.unique_id

	def get_pair_id(self, site1, site2):
		pair_obj = Pair(site1, site2)
		if pair_obj in self.pair_to_id.keys():
			return self.pair_to_id[pair_obj]
		else:
			new_id = self.get_unique_id()
			self.pair_to_id[pair_obj] = new_id
			self.id_to_pair[new_id] = pair_obj
			return new_id


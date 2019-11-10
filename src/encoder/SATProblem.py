# SATProblem Class
from src.encoder.boolean.Pair import Pair
from src.common.BindingSite import BindingSite
from src.common.Monomer import Monomer
from src.encoder.boolean.Bind import Bind

class SATProblem:
	# CONSTRUCTOR
	def __init__(self):
		self.clauses = list()
		self.result = list()
		# string of boolean representation to object
		self.pair_to_id = dict()
		self.id_to_pair = dict()

		self.bind_to_id = dict()
		self.id_to_bind = dict()

		self.unique_id = 0

	def add_clause(self, clause):
		self.clauses.append(clause)

	def get_unique_id(self):
		self.unique_id += 1
		return self.unique_id

	def get_pair_id(self, site1: BindingSite, site2: BindingSite):
		pair_obj = Pair(site1, site2)
		if pair_obj in self.pair_to_id.keys():
			return self.pair_to_id[pair_obj]
		else:
			new_id = self.get_unique_id()
			self.pair_to_id[pair_obj] = new_id
			self.id_to_pair[new_id] = pair_obj
			return new_id

	def get_bind_id(self, monomer1: Monomer, monomer2: Monomer):
		bind_obj = Bind(monomer1, monomer2)
		if bind_obj in self.bind_to_id.keys():
			return self.bind_to_id[bind_obj]
		else:
			new_id = self.get_unique_id()
			self.bind_to_id[bind_obj] = new_id
			self.id_to_bind[new_id] = bind_obj
			return new_id

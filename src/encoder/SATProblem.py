# SATProblem Class
from src.encoder.boolean.Pair import Pair
from src.encoder.boolean.Bind import Bind
from src.encoder.boolean.Rep import Rep
from src.encoder.boolean.Sum import Sum
from src.common.BindingSite import BindingSite
from src.common.Monomer import Monomer
from pysat.solvers import Glucose4


class SATProblem:
	# CONSTRUCTOR
	def __init__(self):
		self.clauses = list()
		self.result = list()
		self.success = True
		self.unique_id = 0
		self.min_reps = 0

		# Pair maps
		self.pair_to_id = dict()
		self.id_to_pair = dict()

		# Bind maps
		self.bind_to_id = dict()
		self.id_to_bind = dict()

		# Representative maps
		self.rep_to_id = dict()
		self.id_to_rep = dict()
		self.rep_list = []

		# We are one indexing
		self.rep_list.append(None)

		# Sum maps
		self.sum_to_id = dict()
		self.id_to_sum = dict()

	def add_clause(self, clause):
		self.clauses.append(clause)

	def increment_min_reps(self):
		self.min_reps += 1

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

	def does_bind_exist(self, monomer1: Monomer, monomer2: Monomer):
		bind_obj = Bind(monomer1, monomer2)
		return bind_obj in self.bind_to_id.keys()

	def get_bind_id(self, monomer1: Monomer, monomer2: Monomer):
		bind_obj = Bind(monomer1, monomer2)
		if bind_obj in self.bind_to_id.keys():
			return self.bind_to_id[bind_obj]
		else:
			new_id = self.get_unique_id()
			self.bind_to_id[bind_obj] = new_id
			self.id_to_bind[new_id] = bind_obj
			return new_id

	def get_rep_id(self, monomer: Monomer):
		rep_obj = Rep(monomer)
		if rep_obj in self.rep_to_id.keys():
			return self.rep_to_id[rep_obj]
		else:
			new_id = self.get_unique_id()
			self.rep_to_id[rep_obj] = new_id
			self.id_to_rep[new_id] = rep_obj
			self.rep_list.append(rep_obj)
			return new_id

	def get_sum_id(self, rep_index, min_reps):
		sum_obj = Sum(rep_index, min_reps)
		if sum_obj in self.sum_to_id.keys():
			return self.sum_to_id[sum_obj]
		else:
			new_id = self.get_unique_id()
			self.sum_to_id[sum_obj] = new_id
			self.id_to_sum[new_id] = sum_obj
			return new_id

	def solve(self):
		solver = Glucose4()

		# solver = Maplesat()
		# solver = Lingeling()
		# solver = Cadical()

		for clause in self.clauses:
			solver.add_clause(clause)

		success = solver.solve()
		if success:
			self.result = solver.get_model()

		self.success = success

# SATProblem Class
from stableconfigs.encoder.boolean.Pair import Pair
from stableconfigs.encoder.boolean.Bind import Bind
from stableconfigs.encoder.boolean.Rep import Rep
from stableconfigs.encoder.boolean.Sum import Sum
from stableconfigs.common.BindingSite import BindingSite
from stableconfigs.common.Monomer import Monomer
from pysat.solvers import Glucose4


class SATProblem:
	# CONSTRUCTOR
	def __init__(self):

		# Seperate each types of clauses into different lists
		self.each_site_binds_at_most_once_clauses = list()
		self.limited_site_binds_clauses = list()
		self.pair_implies_bind_clauses = list()
		self.bind_transitive_clauses = list()
		self.bind_representatives_clauses = list()
		self.increment_min_representatives_clauses = list()
		self.constraint_clauses = list()
		self.unique_combination_clauses = list()

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

		# Original Binds
		self.original_binds = set()

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

	def does_pair_exist(self, site1: BindingSite, site2: BindingSite):
		pair_obj = Pair(site1, site2)
		return pair_obj in self.pair_to_id.keys()

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

	# Reset clauses for a rerun without re-encoding all clauses
	def reset_clauses(self):
		self.increment_min_representatives_clauses = list()
		self.success = True
		self.min_reps = 0
		self.result = list()


	def add_clauses_to_solver(self, solver, constraints_flag: bool):
		for clause in self.each_site_binds_at_most_once_clauses:
			solver.add_clause(clause)

		for clause in self.limited_site_binds_clauses:
			solver.add_clause(clause)

		for clause in self.each_site_binds_at_most_once_clauses:
			solver.add_clause(clause)

		for clause in self.limited_site_binds_clauses:
			solver.add_clause(clause)

		for clause in self.pair_implies_bind_clauses:
			solver.add_clause(clause)

		for clause in self.bind_transitive_clauses:
			solver.add_clause(clause)

		for clause in self.bind_representatives_clauses:
			solver.add_clause(clause)

		for clause in self.increment_min_representatives_clauses:
			solver.add_clause(clause)
		
		for clause in self.unique_combination_clauses:
			solver.add_clause(clause)

		# Only add constraints flag if enabled 
		if constraints_flag: 
			for clause in self.constraint_clauses:
				solver.add_clause(clause)

	def solve(self, constraints_flag = False):
		solver = Glucose4()

		# solver = Maplesat()
		# solver = Lingeling()
		# solver = Cadical()

		self.add_clauses_to_solver(solver, constraints_flag)

		success = solver.solve()
		if success:
			self.result = solver.get_model()

		self.success = success

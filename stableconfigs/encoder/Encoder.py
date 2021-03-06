# class for Encoding/adding clauses to a SATProblem
from stableconfigs.common.TBNProblem import TBNProblem
from stableconfigs.encoder.SATProblem import SATProblem
from stableconfigs.common.Constraint import Constraint, CONSTR
from stableconfigs.common.CustomExceptions import *

# Helper function that runs all basic functions
def encode_basic_clause(tbn: TBNProblem, sat: SATProblem):
	encode_each_site_binds_at_most_once(tbn, sat)
	encode_limiting_site_binds(tbn, sat)
	encode_pair_implies_bind(tbn, sat)
	encode_bind_transitive(tbn, sat)
	encode_bind_representatives(tbn, sat)
	encode_constraints_clauses(tbn, sat)

# Encoding Saturated Configs
# Ensure a binding site binds to at most one other binding site
def encode_each_site_binds_at_most_once(tbn: TBNProblem, sat: SATProblem):
	for site_type in tbn.site_type_to_sitelist_map.keys():
		normal_sites = tbn.site_type_to_sitelist_map[site_type].get_normal_sites()
		complement_sites = tbn.site_type_to_sitelist_map[site_type].get_complement_sites()

		# ensures each complement(*) site binds at most once to any possible suitable binding site (no *)
		for complement_site in complement_sites:
			for site1 in normal_sites:
				for site2 in normal_sites:
					if site1.id < site2.id:
						pair_id_1 = sat.get_pair_id(complement_site, site1)
						pair_id_2 = sat.get_pair_id(complement_site, site2)
						
						# ~Pair(s, t) ∨ ~Pair(s, u) ==> "at most one"
						clause = create_clause(-pair_id_1, -pair_id_2)
						sat.each_site_binds_at_most_once_clauses.append(clause)

		# ensures each non complement site (no *) binds at most once to any possible suitable binding site (*)
		for normal_site in normal_sites:
			for site1 in complement_sites:
				for site2 in complement_sites:
					if site1.id < site2.id:
						pair_id_1 = sat.get_pair_id(normal_site, site1)
						pair_id_2 = sat.get_pair_id(normal_site, site2)

						# ~Pair(s, t) ∨ ~Pair(s, u) ==> "at most one"
						clause = create_clause(-pair_id_1, -pair_id_2)
						sat.each_site_binds_at_most_once_clauses.append(clause)


# Ensure each limiting binding site is binded 
def encode_limiting_site_binds(tbn: TBNProblem, sat: SATProblem):
	for site_type in tbn.site_type_to_sitelist_map.keys():
		limiting_sites, non_limiting_sites = tbn.site_type_to_sitelist_map[site_type].get_limiting_site_and_non_limiting_site()

		for limiting_site in limiting_sites:
			pair_id_list = []
			for non_limiting_site in non_limiting_sites:
				pair_id_list.append(sat.get_pair_id(limiting_site, non_limiting_site))

			# {Pair(s, t) : t ∈ C(s)} ==> "at least one"
			clause = create_clause(*pair_id_list)
			sat.limited_site_binds_clauses.append(clause)


# Encode a pair of two sites will bind the two monomers
def encode_pair_implies_bind(tbn: TBNProblem, sat: SATProblem):
	for pair in sat.pair_to_id.keys():
		pair_id = sat.pair_to_id.get(pair)
		bind_id = sat.get_bind_id(pair.site1.ParentMonomer, pair.site2.ParentMonomer)
		sat.original_binds.add(bind_id)

		# Pair(s, t) → Bind(m, n) ==> ""
		clause = create_clause(-pair_id, bind_id)
		sat.pair_implies_bind_clauses.append(clause)

# Encode the transitive property of Binds
def encode_bind_transitive(tbn: TBNProblem, sat: SATProblem):
	visited_binds = set()
	available_binds = []

	for bind in sat.bind_to_id.keys():
		available_binds.append(bind)

	# available_binds and visited_binds will ensure we don't perform repetitive comparisons
	while len(available_binds) > 0:
		available_bind = available_binds.pop(0)

		for visited_bind in visited_binds:
			
			# Symmetric difference will return the difference monomer set of two Binds
			diff_list = list(available_bind.get_symmetric_difference(visited_bind))
			
			# diff_list of length 2 implies that the Binds shared one common monomer
			if len(diff_list) == 2:

				available_bind_id = sat.bind_to_id.get(available_bind)
				visited_bind_id = sat.bind_to_id.get(visited_bind)

				created_new_bind = False
				if not sat.does_bind_exist(diff_list[0], diff_list[1]):
					created_new_bind = True

				new_bind_id = sat.get_bind_id(diff_list[0], diff_list[1])

				# Bind(m, n) ∧ Bind(m, r) → Bind(n, r) ==> Two overlapping binds implies another bind
				clause = create_clause(-available_bind_id, -visited_bind_id, new_bind_id)				
				sat.bind_transitive_clauses.append(clause)

				# Only add newly created binds to queue
				if created_new_bind:
					available_binds.append(sat.id_to_bind.get(new_bind_id))

		visited_binds.add(available_bind)


def encode_bind_representatives(tbn: TBNProblem, sat: SATProblem):
	# Generate all representatives
	for monomer in tbn.all_monomers:
		sat.get_rep_id(monomer)

	for bind, bind_id in sat.bind_to_id.items():
		max_monomer = bind.monomer1.get_max(bind.monomer2)
		rep_id = sat.get_rep_id(max_monomer)

		# Bind(m, n) → ~Rep(n) ==> A Bind(m, n), where m < n, forces n to not be a representative
		clause = create_clause(-bind_id, -rep_id)
		sat.bind_representatives_clauses.append(clause)

# Encoding is enforcing the configuration to have at least k polymers 
def increment_min_representatives(tbn: TBNProblem, sat: SATProblem):
	
	sat.increment_min_reps()

	# rep_list is 1-indexed for readability
	for rep_index in range(1, len(sat.rep_list)):

		sum_id = sat.get_sum_id(rep_index, sat.min_reps)
		rep_id = sat.rep_to_id.get(sat.rep_list[rep_index])

		# Base case for first rep and k = 1
		if sat.min_reps == 1:
			if rep_index == 1:
				# The first Sum(1, 1) is true if Rep(1) is true
				# Sum(1, 1) → Rep(1) 
				clause = create_clause(-sum_id, rep_id)
				sat.increment_min_representatives_clauses.append(clause)
			else:
				sum_id_previous_sum = sat.get_sum_id(rep_index - 1, sat.min_reps)
				
				# The first row Sum(n, 1) is true if Sum (n - 1, 1) is true or Rep(n) is true
				# Sum(n, 1) → Sum(n - 1, 1) V Rep(n) 
				clause = create_clause(-sum_id, sum_id_previous_sum, rep_id)
				sat.increment_min_representatives_clauses.append(clause)

		# top left triangle are all false
		elif rep_index < sat.min_reps:
			# Sum(n, k) is false for n < k
			clause = create_clause(-sum_id)
			sat.increment_min_representatives_clauses.append(clause)

		else:
			# Sum(n - 1, k)
			sum_id_previous_sum = sat.get_sum_id(rep_index - 1, sat.min_reps)
			
			# Sum(n - 1, k - 1)
			sum_id_diagonal_sum = sat.get_sum_id(rep_index - 1, sat.min_reps - 1)

			# Sum(n, k) -> (Sum(n - 1, k - 1) AND Rep(n))  V  Sum(n - 1, k) 
			# Need to decompose into cnf form due to constraints of SAT Solvers:
			
			# ~Sum(n, k) V Sum(n - 1, k - 1) V Sum(n - 1, k)
			clause = create_clause(-sum_id, sum_id_diagonal_sum, sum_id_previous_sum)
			sat.increment_min_representatives_clauses.append(clause)
			# ~Sum(n, k) V Rep(n) V Sum(n - 1, k)
			clause = create_clause(-sum_id, rep_id, sum_id_previous_sum)
			sat.increment_min_representatives_clauses.append(clause)

	# Ensures Sum(n, k) is true to propogate implies logic from previous clauses 
	sum_id = sat.get_sum_id(len(sat.rep_list) - 1, sat.min_reps)
	sat.increment_min_representatives_clauses.append(create_clause(sum_id))


# Encodes additional constraints into clauses
def encode_constraints_clauses(tbn: TBNProblem, sat: SATProblem):
	for constraint in tbn.constraints:
		
		# TOGETHER: Force monomers into the same polymer
		if constraint.c_type == CONSTR.TOGETHER:
			
			# Compare every combination of monomers
			visited_monomers = set()
			for monomer_name in constraint.arguments:
				mono = tbn.monomer_name_map.get(monomer_name)

				for other_mon in visited_monomers:
					if sat.does_bind_exist(mono, other_mon):
						bind_id = sat.get_bind_id(mono, other_mon)
						clause = create_clause(bind_id)
						sat.constraint_clauses.append(clause)
					
					else:
						# Exception because there is no possible path for monomers to be bound together
						raise TogetherConstraintException(constraint, mono, other_mon)

				visited_monomers.add(mono)

		# NOTTOGETHER: Prevents two monomers from being in the same polymer
		elif constraint.c_type == CONSTR.NOTTOGETHER:
			mono = tbn.monomer_name_map.get(constraint.arguments[0])
			other_mon = tbn.monomer_name_map.get(constraint.arguments[1])
			
			if sat.does_bind_exist(mono, other_mon):
				bind_id = sat.get_bind_id(mono, other_mon)
				clause = create_clause(-bind_id)
				sat.constraint_clauses.append(clause)

		# FREE: Force monomer to not bind to any other monomer
		elif constraint.c_type == CONSTR.FREE:
			# Set every bind to false for that monomer
			for monomer_name in constraint.arguments:
				mono = tbn.monomer_name_map.get(monomer_name)

				for other_mon in tbn.all_monomers:
					if (sat.does_bind_exist(mono, other_mon)):
						bind_id = sat.get_bind_id(mono, other_mon)
						# Set bind clause to false
						clause = create_clause(-bind_id)
						sat.constraint_clauses.append(clause)
		
		#NOTFREE: Force specified monomer to bind to any other monomers
		elif constraint.c_type == CONSTR.NOTFREE:
			monomer_name = constraint.arguments[0]
			mono = tbn.monomer_name_map.get(monomer_name)

			potential_binds = []
			for other_mon in tbn.all_monomers:
				if sat.does_bind_exist(mono, other_mon):
					bind_id = sat.get_bind_id(mono, other_mon)
					potential_binds.append(bind_id)

			# If there exists no binds, then we force unsat
			if len(potential_binds) == 0:
				raise NotFreeConstraintException(constraint, mono)

			else:
				clause = create_clause(*potential_binds)
				sat.constraint_clauses.append(clause)

		#PAIRED: Forces two binding sites to bind together
		elif constraint.c_type == CONSTR.PAIRED:
			bsite = tbn.bindingsite_name_map.get(constraint.arguments[0])
			other_bsite = tbn.bindingsite_name_map.get(constraint.arguments[1])

			if sat.does_pair_exist(bsite, other_bsite):
				pair_id = sat.get_pair_id(bsite, other_bsite)
				clause = create_clause(pair_id)
				sat.constraint_clauses.append(clause)
			else:
				raise PairedConstraintException(constraint, bsite, other_bsite)				
		
		elif constraint.c_type == CONSTR.NOTPAIRED:
			bsite = tbn.bindingsite_name_map.get(constraint.arguments[0])
			other_bsite = tbn.bindingsite_name_map.get(constraint.arguments[1])
		
			if sat.does_pair_exist(bsite, other_bsite):
				pair_id = sat.get_pair_id(bsite, other_bsite)
				clause = create_clause(-pair_id)
				sat.constraint_clauses.append(clause)
			else:
				# Can ignore because will not cause UNSAT.
				pass

		elif constraint.c_type == CONSTR.ANYPAIRED:
			bsite = tbn.bindingsite_name_map.get(constraint.arguments[0])
			if bsite.IsComplement:
				other_binds = tbn.site_type_to_sitelist_map[bsite.type].get_normal_sites()
			else:
				other_binds = tbn.site_type_to_sitelist_map[bsite.type].get_complement_sites()

			if len(other_binds) != 0:
				potential_binds = []
				for other_bsite in other_binds:
					pair_id = sat.get_pair_id(bsite, other_bsite)
					potential_binds.append(pair_id)
				
				clause = create_clause(*potential_binds)
				sat.constraint_clauses.append(clause)
			else:
				raise AnyPairedConstraintException(constraint, bsite)

		
		elif constraint.c_type == CONSTR.NOTANYPAIRED:
			bsite = tbn.bindingsite_name_map.get(constraint.arguments[0])
			if bsite.IsComplement:
				other_binds = tbn.site_type_to_sitelist_map[bsite.type].get_normal_sites()
			else:
				other_binds = tbn.site_type_to_sitelist_map[bsite.type].get_complement_sites()

			if len(other_binds) != 0:
				for other_bsite in other_binds:
					pair_id = sat.get_pair_id(bsite, other_bsite)
					clause = create_clause(-pair_id)
					sat.constraint_clauses.append(clause)
			else:
				# Can ignore because will not cause UNSAT.
				pass
		
		else:
			# TODO: Should never enter here, default is to ignore.
			
			pass


# Encodes a unique solution combination
def encode_unique_solution(tbn : TBNProblem, sat : SATProblem):
	true_pairs = []
	for boolean in sat.result:
		if boolean > 0 and boolean in sat.id_to_pair.keys():
			# Adds constraints to not produce the original solution again
			true_pairs.append(boolean * -1)

	# Adds new clause
	clause = create_clause(*true_pairs)
	sat.unique_combination_clauses.append(clause)


def create_clause(*args):
	clause = []
	for argument in args:
		clause.append(argument)
	return clause

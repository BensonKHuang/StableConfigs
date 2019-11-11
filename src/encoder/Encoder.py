#class for Encoding/adding clauses to a SATProblem
from src.common.TBNProblem import TBNProblem 
from src.encoder.boolean.Pair import Pair
from src.common.SiteList import SiteList
from src.encoder.SATProblem import SATProblem

###generateBasicClauses(solution) 	
#eachSiteBindsAtMostOnce(solution) ------> for every site, can bind to at max 1  	
#eachLimitingSiteBinds(solution) ------> each limiting site bound 	
#pairImpliesBind(solution) -----> generates bind objects and pair->bind clauses 	
#bindRep(solution) -> bind rep relationship clause  incrementK(solution)  	
#modify clauses for the sum(n,k) table

def encode_basic_clause(tbn : TBNProblem, sat : SATProblem):
	encode_each_site_binds_at_most_once(tbn, sat)
	encode_limiting_site_binds(tbn, sat)
	encode_pair_implies_bind(tbn, sat)
	encode_bind_transitive(tbn, sat)
	encode_bind_representatives(tbn, sat)

def encode_each_site_binds_at_most_once(tbn : TBNProblem, sat : SATProblem):
	for site_type in tbn.site_name_to_sitelist_map.keys():
		normal_sites = tbn.site_name_to_sitelist_map[site_type].get_normal_sites()
		complement_sites = tbn.site_name_to_sitelist_map[site_type].get_complement_sites()

		#ensures each complement(*) site binds at most once to any possible suitable binding site (no *)
		for complement_site in complement_sites:
			for site1 in normal_sites:
				for site2 in normal_sites:
					if site1.id < site2.id:
						pairID1 = sat.get_pair_id(complement_site, site1)
						pairID2 = sat.get_pair_id(complement_site, site2)
						clause = create_clause(-pairID1, -pairID2)
						sat.add_clause(clause)

		#ensures each non complement site (no *) binds at most once to any possible suitable binding site (*)				
		for normal_site in normal_sites:
			for site1 in complement_sites:
				for site2 in complement_sites:
					if site1.id < site2.id:
						pairID1 = sat.get_pair_id(normal_site, site1)
						pairID2 = sat.get_pair_id(normal_site, site2)
						clause = create_clause(-pairID1, -pairID2)
						sat.add_clause(clause)


def encode_limiting_site_binds(tbn : TBNProblem, sat : SATProblem):
	for site_type in tbn.site_name_to_sitelist_map.keys():
		limiting_sites, non_limiting_sites = tbn.site_name_to_sitelist_map[site_type].get_limiting_site_and_non_limiting_site()

		for limiting_site in limiting_sites:
			pair_id_list = []
			for non_limiting_site in non_limiting_sites:
				pair_id_list.append(sat.get_pair_id(limiting_site, non_limiting_site))

			clause = create_clause(*pair_id_list)
			sat.add_clause(clause)


def encode_pair_implies_bind(tbn : TBNProblem, sat : SATProblem):
	for pair in sat.pair_to_id.keys():
		pair_id = sat.pair_to_id.get(pair)
		bind_id = sat.get_bind_id(pair.site1.ParentMonomer, pair.site2.ParentMonomer)

		clause = create_clause(-pair_id, bind_id)
		sat.add_clause(clause)


def encode_bind_transitive(tbn : TBNProblem, sat : SATProblem):
	original_binds = dict(sat.bind_to_id).items()

	for bind1, bind1_id in original_binds:
		for bind2, bind2_id in original_binds:
			if bind1_id < bind2_id:
				diff_list = list(bind1.get_symmetric_difference(bind2))
				if len(diff_list) == 2:
					new_bind_id = sat.get_bind_id(diff_list[0], diff_list[1])

					clause = create_clause(-bind1_id, -bind2_id, new_bind_id)
					sat.add_clause(clause)


def encode_bind_representatives(tbn : TBNProblem, sat : SATProblem):
	# Generate all representatives
	for monomer in tbn.all_monomers:
		sat.get_rep_id(monomer)

	for bind, bind_id in sat.bind_to_id.items():
		max_monomer = bind.monomer1.get_max(bind.monomer2)
		rep_id = sat.get_rep_id(max_monomer)
		clause = create_clause(-bind_id, -rep_id)
		sat.add_clause(clause)


def increment_min_representatives(tbn : TBNProblem, sat : SATProblem):

	sat.increment_min_reps()

	for rep_index in range(1, len(sat.rep_list)):

		sum_id = sat.get_sum_id(rep_index, sat.min_reps)
		rep_id = sat.rep_to_id.get(sat.rep_list[rep_index])

		# Base case for first rep and k = 1
		if sat.min_reps == 1:
			if rep_index == 1:
				sat.add_clause(create_clause(-sum_id, rep_id))
			else:
				sum_id_previous_sum = sat.get_sum_id(rep_index - 1, sat.min_reps)
				sat.add_clause(create_clause(-sum_id, sum_id_previous_sum, rep_id))

		# top left triangle are all false
		elif rep_index < sat.min_reps:
			sat.add_clause(create_clause(-sum_id))

		else:
			# sum(n, k) -> (sum(n - 1, k - 1) and rep(n)) V sum(n - 1, k)
			sum_id_previous_sum = sat.get_sum_id(rep_index - 1, sat.min_reps)
			sum_id_diagonal_sum = sat.get_sum_id(rep_index - 1, sat.min_reps - 1)

			# Add two clauses for cnf form:

			# ~sum(n, k) V sum(n - 1, k - 1) V sum(n - 1, k)
			sat.add_clause(create_clause(-sum_id, sum_id_diagonal_sum, sum_id_previous_sum))
			# ~sum(n, k) V rep(n) V sum(n - 1, k)
			sat.add_clause(create_clause(-sum_id, rep_id, sum_id_previous_sum))

	sum_id = sat.get_sum_id(len(sat.rep_list) - 1, sat.min_reps)
	sat.add_clause(create_clause(sum_id))


def create_clause(*args):
	clause = []
	for argument in args:
		clause.append(argument)
	return clause

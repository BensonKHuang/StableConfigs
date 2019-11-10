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


def encode_each_site_binds_at_most_once(tbn : TBNProblem, sat : SATProblem):
	for site_type in tbn.site_name_to_sitelist_map.keys():
		normal_sites = tbn.site_name_to_sitelist_map[site_type].get_normal_sites()
		complement_sites = tbn.site_name_to_sitelist_map[site_type].get_complement_sites()

		#ensures each complement(*) site binds at most once to any possible suitable binding site (no *)
		for complement_site in complement_sites:
			for pair1 in normal_sites:
				for pair2 in normal_sites:
					if pair1.id < pair2.id:
						pairID1 = sat.get_pair_id(complement_site, pair1)
						pairID2 = sat.get_pair_id(complement_site, pair2)
						clause = create_clause(-pairID1, -pairID2)
						sat.add_clause(clause)

		#ensures each non complement site (no *) binds at most once to any possible suitable binding site (*)				
		for normal_site in normal_sites:
			for pair1 in complement_sites:
				for pair2 in complement_sites:
					if pair1.id < pair2.id:
						pairID1 = sat.get_pair_id(normal_site, pair1)
						pairID2 = sat.get_pair_id(normal_site, pair2)
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
	return True


def add_k_clause(tbn : TBNProblem, sa : SATProblem):
	return True


def create_clause(*args):
	clause = []
	for argument in args:
		clause.append(argument)
	return clause

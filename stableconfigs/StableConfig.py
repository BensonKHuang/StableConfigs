from stableconfigs.parser.Parser import parse_input_lines
from stableconfigs.encoder.SATProblem import SATProblem
import stableconfigs.encoder.Encoder as Encoder
import stableconfigs.decoder.Decoder as Decoder
import time


def get_stable_config(tbn_lines, constr_lines, gen_count, init_k):
    # parse the input to encode it into BindingSite/Monomer classes
    
    t0 = time.time()
    tbn_problem = parse_input_lines(tbn_lines, constr_lines)

    tbn_problem.gen_count = gen_count
    tbn_problem.init_k = init_k
    configs = []

    # encode problem to SAT solver compatible problem
    sat_problem = SATProblem()
    Encoder.encode_basic_clause(tbn_problem, sat_problem)
    print("\nCOMPUTING ORIGINAL STABLE CONFIGURATION:")

    while sat_problem.min_reps < tbn_problem.init_k:
        Encoder.increment_min_representatives(tbn_problem, sat_problem)
    
    original_num_reps = 0

    # solve the problem (SAT solver)
    while sat_problem.success:
        print("... Checking for k =", sat_problem.min_reps, "polymers")
        sat_problem.solve()
        if (sat_problem.success):
            original_num_reps = sat_problem.min_reps
            Encoder.increment_min_representatives(tbn_problem, sat_problem)

    if original_num_reps > 0:
        print("Found an original stable configuration with [", original_num_reps, "] polymers.\n")
    else:   
        print("Could not find original stable configuration with [", tbn_problem.init_k, "] polymers.\n")
        # Printing execution time
        print("\nCompleted in", time.time() - t0, "seconds.\n")
        return configs

    # Add constraints set clauses and solve specified number of times
    if len(tbn_problem.constraints) != 0:
        print("\nCOMPUTING STABLE CONFIGURATION WITH ADDITIONAL CONSTRAINTS:")
        Encoder.encode_constraints_clauses(tbn_problem, sat_problem)
        configs = get_stable_configs_using_constraints(
            tbn_problem, sat_problem, original_num_reps)

    # Generate more than one solution with no additional constraints
    elif tbn_problem.gen_count > 1:
        configs = get_stable_configs_using_constraints(
            tbn_problem, sat_problem, original_num_reps)
    else:
        # Decode the problem into polymers
        polymers = Decoder.decode_boolean_values(tbn_problem, sat_problem)
        configs.append(polymers)
        for index, polymer in enumerate(polymers):
            print("\t" + "Polymer number", index + 1)
            for monomer in polymer.monomer_list:
                print("\t\t" + str(monomer))
            print()
    
    # Printing execution time
    print("\nCompleted in", time.time() - t0, "seconds.\n")
    return configs


def get_stable_configs_using_constraints(tbn_problem, sat_problem, original_num_reps):
    counter = 0
    configs = []
    # Generate multiple unique solutions
    while counter < tbn_problem.gen_count:
        sat_problem.reset_clauses()
        
        while sat_problem.min_reps < tbn_problem.init_k:
            Encoder.increment_min_representatives(tbn_problem, sat_problem)

        modified_num_reps = 0
        
        # solve the problem again (SAT solver)
        while sat_problem.success:
            print("... Checking for k =", sat_problem.min_reps, "polymers")
            sat_problem.solve()
            if (sat_problem.success):
                modified_num_reps = sat_problem.min_reps
                Encoder.increment_min_representatives(tbn_problem, sat_problem)

        if modified_num_reps > 0:
            print("Found a constrained stable configuration with [", modified_num_reps, "] polymers.\n")
            print("Entropy is [", original_num_reps - modified_num_reps, "] away from stable configuration:\n")
        else:
            print("Unsatisfiable\n")
            break

        # Decode the problem into polymers
        polymers = Decoder.decode_boolean_values(tbn_problem, sat_problem)
        configs.append(polymers)
        for index, polymer in enumerate(polymers):
            print("\t" + "Polymer number", index + 1)
            for monomer in polymer.monomer_list:
                print("\t\t" + str(monomer))
            print()

        print("Constraints:")
        for constr in tbn_problem.constraints:
            print("\t" + str(constr))
        print()
        # Encode a new unique solution
        Encoder.encode_unique_solution(tbn_problem, sat_problem)
        counter += 1
    return configs

from stableconfigs.parser.Parser import parse_input_lines
from stableconfigs.encoder.SATProblem import SATProblem
from stableconfigs.common.TBNProblem import TBNProblem
from stableconfigs.common.CustomExceptions import *
import stableconfigs.encoder.Encoder as Encoder
import stableconfigs.decoder.Decoder as Decoder
import time


def get_stable_config(tbn_lines, constr_lines, gen_count, init_k, celery_task = None):
    # parse the input to encode it into BindingSite/Monomer classes

    t0 = time.time()
    # Celery Task is flag to indicate if a call is made from library or from a celery broker worker API
    if celery_task is not None:

        if celery_task.is_aborted():
            raise EarlyTerminationException(0, 0)

        celery_task.update_state(state="PROGRESS",
            meta={'status': "Progress", 'count': 0, 'k': 0})

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
        
        if celery_task is not None:
            
            if celery_task.is_aborted():
                raise EarlyTerminationException(1, sat_problem.min_reps)

            celery_task.update_state(state="PROGRESS",
                meta={'status': "Progress", 'count': 1, 'k': sat_problem.min_reps})
        if celery_task is None:
            print("... Checking for k =", sat_problem.min_reps, "polymers")
        sat_problem.solve(False)
        if (sat_problem.success):
            original_num_reps = sat_problem.min_reps
            Encoder.increment_min_representatives(tbn_problem, sat_problem)

    if original_num_reps > 0:
        if celery_task is None:
            print("Found an original stable configuration with [", original_num_reps, "] polymers.\n")
    else:  
        if celery_task is None:
            print("Could not find original stable configuration with [", tbn_problem.init_k, "] polymers.\n")
            # Printing execution time
            print("\nCompleted in", time.time() - t0, "seconds.\n")
        raise MinPolymersExceedEntropyException(tbn_problem.init_k)

    # Add constraints set clauses and solve specified number of times
    if len(tbn_problem.constraints) != 0:
        print("\nCOMPUTING STABLE CONFIGURATION WITH ADDITIONAL CONSTRAINTS:")
        configs = get_stable_configs_using_constraints(
            tbn_problem, sat_problem, original_num_reps, celery_task)

    # Generate more than one solution with no additional constraints
    elif tbn_problem.gen_count > 1:
        configs = get_stable_configs_using_constraints(
            tbn_problem, sat_problem, original_num_reps, celery_task)
    else:
        # Decode the problem into polymers
        polymers = Decoder.decode_boolean_values(tbn_problem, sat_problem)
        configs.append(polymers)
        if celery_task is None:
            for index, polymer in enumerate(polymers):
                print("\t" + "Polymer number", index + 1)
                for monomer in polymer.monomer_list:
                    print("\t\t" + str(monomer))
                print()
    
    # Printing execution time
    if celery_task is None:
        print("\nCompleted in", time.time() - t0, "seconds.\n")
    
    return configs, original_num_reps


def get_stable_configs_using_constraints(tbn_problem, sat_problem, original_num_reps, celery_task = None):
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

            if celery_task is not None:
                
                if celery_task.is_aborted():
                    raise EarlyTerminationException(counter + 1, sat_problem.min_reps)

                celery_task.update_state(state="PROGRESS",
                    meta={'status': "Progress",  'count': counter + 1, 'k': sat_problem.min_reps})
            if celery_task is None:
                print("... Checking for k =", sat_problem.min_reps, "polymers")
            sat_problem.solve(True)
            if (sat_problem.success):
                modified_num_reps = sat_problem.min_reps
                Encoder.increment_min_representatives(tbn_problem, sat_problem)
        if modified_num_reps > 0:
            if celery_task is None:
                print("Found a constrained stable configuration with [", modified_num_reps, "] polymers.\n")
                print("Entropy is [", original_num_reps - modified_num_reps, "] away from stable configuration:\n")
        else:
            print("Unsatisfiable\n")
            break

        # Decode the problem into polymers
        polymers = Decoder.decode_boolean_values(tbn_problem, sat_problem)
        configs.append(polymers)

        if celery_task is None:
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

def config_to_output(config):
    polymer_output = []
    for index, polymer in enumerate(config):
        polymer_output.append(polymer.to_json_format())
    return polymer_output, len(polymer_output)

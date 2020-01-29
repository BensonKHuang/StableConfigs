from stableconfigs.parser.Parser import parse_input_file
from stableconfigs.encoder.SATProblem import SATProblem
import stableconfigs.encoder.Encoder as Encoder
import stableconfigs.decoder.Decoder as Decoder
import time


def get_stable_config(file_path, instr_path):
    # parse the input to encode it into BindingSite/Monomer classes
    
    t0 = time.time()
    tbn_problem = parse_input_file(file_path, instr_path)

    # encode problem to SAT solver compatible problem
    sat_problem = SATProblem()
    Encoder.encode_basic_clause(tbn_problem, sat_problem)

    # solve the problem (SAT solver)
    while sat_problem.success:
        Encoder.increment_min_representatives(tbn_problem, sat_problem)
        print("[Checking for k =", sat_problem.min_reps, "polymers]")
        sat_problem.solve()

    # Formatting for printing
    print()
    num_reps = sat_problem.min_reps - 1
    if num_reps > 0:
        print("Found a stable configuration with [", num_reps, "] polymers:\n")
    
    # Decode the problem into polymers
    polymers = Decoder.decode_boolean_values(tbn_problem, sat_problem)
    for index, polymer in enumerate(polymers):
        print("\t" + "Polymer number", index + 1)
        for monomer in polymer.monomer_list:
            print("\t\t" + str(monomer))
        print()

    print("Properties:")
    for instr in tbn_problem.instructions:
        print("\t" + str(instr))
    
    # Printing execution time
    print("\nCompleted in", time.time() - t0, "seconds.")

    return polymers

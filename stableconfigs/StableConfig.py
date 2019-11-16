from stableconfigs.parser.Parser import parse_input_file
from stableconfigs.encoder.SATProblem import SATProblem
import stableconfigs.encoder.Encoder as Encoder
import stableconfigs.decoder.Decoder as Decoder
import time


def get_stable_config(file_path):
    # parse the input to encode it into BindingSite/Monomer classes
    
    t0 = time.time()
    tbn_problem = parse_input_file(file_path)

    # encode problem to SAT solver compatible problem
    sat_problem = SATProblem()
    Encoder.encode_basic_clause(tbn_problem, sat_problem)

    # solve the problem (SAT solver)
    while sat_problem.success:
        Encoder.increment_min_representatives(tbn_problem, sat_problem)
        print("[ k =", sat_problem.min_reps, "]")
        sat_problem.solve()

    # Decode the problem into polymers
    polymers = Decoder.decode_boolean_values(tbn_problem, sat_problem)
    for index, polymer in enumerate(polymers):
        print("Polymer number", index + 1)
        for monomer in polymer.monomer_list:
            print("\t" + str(list(map(lambda x: (x.name + "*") if x.IsComplement else x.name, monomer.BindingSites))))

    print("Completed in", time.time() - t0, "seconds.")

    return polymers

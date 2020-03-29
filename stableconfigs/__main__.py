from stableconfigs import StableConfig
from flaskserver import server
import sys
import argparse

if __name__ == '__main__':
    #python3 -m stableconfigs -g 100 input/and_gate.txt  input/and_gate_constr.txt
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', default=1, type=int)
    parser.add_argument('-g', default=1, type=int)
    parser.add_argument('-s', action='store_true', default=False)
    parser.add_argument('rest', nargs=argparse.REMAINDER)
    options = parser.parse_args()

    gen_count = options.g
    init_k = options.k

    if options.s:
        server.run_app()
    else:
        file_path = options.rest[0]
        tbn_file = open(file_path, 'rt')
        tbn_lines = tbn_file.readlines()
        tbn_file.close()

        constr_lines = []
        if len(options.rest) >= 2:
            constr_path = options.rest[1]
            constr_file = open(constr_path, 'rt')
            constr_lines = constr_file.readlines()
            constr_file.close()
        
        StableConfig.get_stable_config(tbn_lines, constr_lines, gen_count, init_k)

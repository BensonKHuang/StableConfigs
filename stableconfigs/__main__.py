from stableconfigs import StableConfig
from bottleServer import server
import sys
import argparse

if __name__ == '__main__':
    #python3 -m stableconfigs -g 100 input/and_gate.txt  input/and_gate_instr.txt
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', default=1, type=int)
    parser.add_argument('-s', action='store_true', default=False)
    parser.add_argument('rest', nargs=argparse.REMAINDER)
    options = parser.parse_args()

    gen_count = options.g

    if options.s:
        server.run_app()
    else:
        file_path = options.rest[0]
        tbn_file = open(file_path, 'rt')
        tbn_lines = tbn_file.readlines()
        tbn_file.close()

        instr_lines = []
        if len(options.rest) >= 2:
            instr_path = options.rest[1]
            instr_file = open(instr_path, 'rt')
            instr_lines = instr_file.readlines()
            instr_file.close()
        
        succ, msg = StableConfig.get_stable_config(tbn_lines, instr_lines, gen_count)
        if not succ:
            pass  # TODO: The error message is here.

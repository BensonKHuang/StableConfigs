from stableconfigs import StableConfig
from bottleServer import server
import sys
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', action='store_true', default=False)
    parser.add_argument('rest', nargs=argparse.REMAINDER)
    options = parser.parse_args()

    if options.s:
        server.run_app()
    else:
        file_path = options.rest[0]
        instr_path = options.rest[1] if len(options.rest) >= 2 else None
        StableConfig.get_stable_config(file_path, instr_path)


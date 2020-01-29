from stableconfigs import StableConfig
from server import server
import sys

if __name__ == '__main__':
    # python3 -m src /home/kyle/StableConfigs/input/wraparound_sorting_network.txt
    API_Debug = False # Set to True for debugging
    if not API_Debug:
        file_path = sys.argv[1]
        instr_path = sys.argv[2] if len(sys.argv) >= 2 else None
        StableConfig.get_stable_config(file_path, instr_path)
    else:
        server.run_app()


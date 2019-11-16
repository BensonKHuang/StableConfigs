from stableconfigs import StableConfig
import sys

if __name__ == '__main__':
    # python3 -m src /home/kyle/StableConfigs/input/wraparound_sorting_network.txt
    
    file_path = sys.argv[1]
    StableConfig.get_stable_config(file_path)

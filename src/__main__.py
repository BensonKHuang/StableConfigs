import src.controller.Controller as Controller
import sys

if __name__ == '__main__':
    # python3 -m src /home/kyle/StableConfigs/input/wraparound_sorting_network.txt
    
    file_path = sys.argv[1]
    Controller.run(file_path)

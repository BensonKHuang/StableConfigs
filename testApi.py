import requests
import os

open_file = open("input/wraparound_sorting_network.txt", "rt")
# open_file = open("input/basic.txt", "rt")

next_line = open_file.readline()
my_mon = []
while next_line:
    tokens = next_line.strip().split(' ')
    my_mon.append(tokens)
    next_line = open_file.readline()
open_file.close()

dicToSend = {'monomers': my_mon}
res = requests.post('http://198.23.133.106:5005/', json=dicToSend)
print(res.json())
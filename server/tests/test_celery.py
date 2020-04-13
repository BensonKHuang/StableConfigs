import requests
import os
import json
import stableconfigs
import time
from stableconfigs.parser.Parser import parse_input_lines

tbn_file = open("../../input/wraparound_sorting_network.txt", 'rt')
my_mon = []
for line in tbn_file.readlines():
    tokens = line.strip().split(' ')
    my_mon.append(tokens)
tbn_file.close()

dicToSend = {'monomers': my_mon, 'gen': 2}
res = requests.post('http://localhost:5005/task', json=dicToSend)
print(str(res.status_code) + ": " + res.text)
task_id = json.loads(res.text)["task_id"]


res = requests.get('http://localhost:5005/status/' + task_id)
print(str(res.status_code) + ": " + res.text)

# res = requests.delete('http://localhost:5005/terminate/' + task_id)
# print(str(res.status_code) + ": " + res.text)

while True:
    res = requests.get('http://localhost:5005/status/' + task_id)
    print(str(res.status_code) + ": " + res.text)
    if res.status_code != 202 and res.status_code != 404:
        break


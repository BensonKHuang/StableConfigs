import requests
import os
import json
import stableconfigs

monomer_input = ["a b >mon1",
                    "a* b* >mon2",
                    "a >mon3",
                    "b >mon4"]
my_mon = []
for line in monomer_input:
    tokens = line.strip().split(' ')
    my_mon.append(tokens)

dicToSend = {'monomers': my_mon, 'gen': 2}
res = requests.post('http://localhost:5005/task', json=dicToSend)
print(res)

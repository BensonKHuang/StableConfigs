import requests
import os
import json
import stableconfigs
import time

monomer_input = ["a b c >mon1",
                    "a* b* c >mon2",
                    "a c* >mon3",
                    "b >mon4",
                    "c*",
                    "a b c*",
                    "d* a",
                    "d c",
                    "c c"]
my_mon = []
for line in monomer_input:
    tokens = line.strip().split(' ')
    my_mon.append(tokens)

dicToSend = {'monomers': my_mon, 'gen': 2}
res = requests.post('http://localhost:5005/task', json=dicToSend)
print("status: " + str(res.status_code))
url = data = json.loads(res.text)["location"]



res = requests.get('http://localhost:5005' + url)
print(res.text)
res = requests.get('http://localhost:5005' + url)
print(res.text)
res = requests.get('http://localhost:5005' + url)
print(res.text)
res = requests.get('http://localhost:5005' + url)
print(res.text)
res = requests.get('http://localhost:5005' + url)
print(res.text)
res = requests.get('http://localhost:5005' + url)
print(res.text)

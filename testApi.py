import requests
import os

open_file = open("input/basic.txt", "rt")

next_line = open_file.readline()
my_mon = []
while next_line:
    tokens = next_line.strip().split(' ')
    my_mon.append(tokens)
    next_line = open_file.readline()
open_file.close()

const_file = open("input/error_constraints.txt", "rt")
next_line = const_file.readline()
my_const = []
while next_line:
    tokens = next_line.strip().split(' ')
    my_const.append(tokens)
    next_line = const_file.readline()
const_file.close()

dicToSend = {'monomers': my_mon, 'constraints': my_const,'gen':3}
res = requests.post('http://localhost:5005/', json=dicToSend)
print(res.status_code)
print(res.text)

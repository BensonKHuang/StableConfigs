import requests
my_mon = [['a', 'b'], ['a*'], ['b*'], ['a*', 'b*']]

dicToSend = {'monomers': my_mon}
res = requests.post('http://198.23.133.106:5005/', json=dicToSend)
print(res.json())
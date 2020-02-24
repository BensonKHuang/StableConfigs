import requests
my_mon = [['a', 'b'], ['a*'], ['b*'], ['a*', 'b*']]

dicToSend = {'monomers': my_mon}
res = requests.post('http://localhost:5000/', json=dicToSend)
print(res.json())
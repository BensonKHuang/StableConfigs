import requests
import os
import json
import unittest
import stableconfigs

class APITest(unittest.TestCase):

    def test_basic_local_server(self):
        
        monomer_input = ["a b >mon1",
        "a* b* >mon2",
        "a >mon3",
        "b >mon4"]
        my_mon = []
        for line in monomer_input:
            tokens = line.strip().split(' ')
            my_mon.append(tokens)

        dicToSend = {'monomers': my_mon, 'gen':2}
        res = requests.post('http://localhost:5005/', json=dicToSend)
        
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.text)
        self.assertEqual(len(data["configs"]), 2)

    def test_basic_with_constraints(self):

        monomer_input = ["a b >mon1",
                         "a* b* >mon2",
                         "a >mon3",
                         "b >mon4"]
        my_mon = []
        for line in monomer_input:
            tokens = line.strip().split(' ')
            my_mon.append(tokens)

        constr_input = ["FREE mon1"]
        my_const = []
        for line in constr_input:
            tokens = line.strip().split(' ')
            my_const.append(tokens)

        dicToSend = {'monomers': my_mon, 'constraints': my_const}
        res = requests.post('http://localhost:5005/', json=dicToSend)

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.text)
        self.assertEqual(data["configs"][0]["polymers_count"], 2)

if __name__ == '__main__':
	unittest.main()

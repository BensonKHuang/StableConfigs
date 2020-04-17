import requests
import os
import json
import unittest
import stableconfigs
import time

class APITest(unittest.TestCase):

    URL = 'http://localhost:5005/'
    START = URL + 'task'
    GETSTATUS = URL + 'status/'
    TERMINATE = URL + 'terminate/'

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
        res = requests.post(self.START, json=dicToSend)
        
        self.assertEqual(res.status_code, 202)
        task_id = json.loads(res.text)["task_id"]
        
        while res.status_code == 202 or res.status_code == 203:
            res = requests.get(self.GETSTATUS + str(task_id))

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.text)
        self.assertEqual(data["count"], 2)
        self.assertEqual(data["entropy"], 3)


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
        res = requests.post(self.START, json=dicToSend)

        self.assertEqual(res.status_code, 202)
        task_id = json.loads(res.text)["task_id"]

        while res.status_code == 202 or res.status_code == 203:
            res = requests.get(self.GETSTATUS + str(task_id))

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.text)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["entropy"], 3)

    def test_empty_error(self):
        monomer_input = []
        my_mon = []
        my_const = []

        dicToSend = {'monomers': my_mon, 'constraints': my_const}
        res = requests.post(self.START, json=dicToSend)

        self.assertEqual(res.status_code, 202)
        task_id = json.loads(res.text)["task_id"]

        while res.status_code == 202 or res.status_code == 203:
            res = requests.get(self.GETSTATUS + str(task_id))

        self.assertEqual(res.status_code, 401)
        data = json.loads(res.text)

        self.assertEqual(data["status"], "TBNException")
        self.assertTrue("Input contains no monomers" in str(data["message"]))

    def test_bsite_anypaired_constraint_exception(self):
        my_mon = [["a:s1"]]
        my_const = [["ANYPAIRED", "s1"]]

        dicToSend = {'monomers': my_mon, 'constraints': my_const}
        res = requests.post(self.START, json=dicToSend)

        self.assertEqual(res.status_code, 202)
        task_id = json.loads(res.text)["task_id"]

        while res.status_code == 202 or res.status_code == 203:
            res = requests.get(self.GETSTATUS + str(task_id))

        self.assertEqual(res.status_code, 401)
        data = json.loads(res.text)

        self.assertEqual(data["status"], "TBNException")
        self.assertTrue("Binding Site [s1]" in str(data["message"]))

    # Flakey Test 
    def test_terminate(self):

        monomer_input = ["a b >mon1",
                         "a* b* >mon2",
                         "a >mon3",
                         "b >mon4"]
        my_mon = []
        for line in monomer_input:
            tokens = line.strip().split(' ')
            my_mon.append(tokens)

        dicToSend = {'monomers': my_mon, 'gen': 1}
        res = requests.post(self.START, json=dicToSend)
        task_id = json.loads(res.text)["task_id"]

        res = requests.delete('http://localhost:5005/terminate/' + task_id)
        self.assertEqual(res.status_code, 200)

        res = requests.get(self.GETSTATUS + task_id)

        while res.status_code == 202 or res.status_code == 203:
            res = requests.get(self.GETSTATUS + str(task_id))
        
        if res.status_code != 200:
            data = json.loads(res.text)
            self.assertEqual(data["status"], "TBNException")
            self.assertTrue("Early Termination" in str(data["message"]))

if __name__ == '__main__':
	unittest.main()

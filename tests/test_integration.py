import unittest
import stableconfigs

from stableconfigs.parser.Parser import parse_input_lines
from stableconfigs.encoder import Encoder
from stableconfigs.encoder.SATProblem import SATProblem


class IntegrationTest(unittest.TestCase):

	def test_basic(self):
		tbn_file = open("../input/basic.txt", 'rt')
		tbn_problem = parse_input_lines(tbn_file.readlines(), [])
		tbn_file.close()
		sat_problem = SATProblem()

		Encoder.encode_basic_clause(tbn_problem, sat_problem)

		while sat_problem.success:
			Encoder.increment_min_representatives(tbn_problem, sat_problem)
			sat_problem.solve()
		self.assertEqual(sat_problem.min_reps, 5)

	def test_and_gate(self):
		tbn_file = open("../input/and_gate.txt", 'rt')
		tbn_problem = parse_input_lines(tbn_file.readlines(), [])
		tbn_file.close()
		sat_problem = SATProblem()

		Encoder.encode_basic_clause(tbn_problem, sat_problem)

		while sat_problem.success:
			Encoder.increment_min_representatives(tbn_problem, sat_problem)
			sat_problem.solve()

		self.assertEqual(sat_problem.min_reps, 6)

	def test_strand_displacement(self):
		tbn_file = open("../input/strand_displacement.txt", 'rt')
		tbn_problem = parse_input_lines(tbn_file.readlines(), [])
		tbn_file.close()
		sat_problem = SATProblem()

		Encoder.encode_basic_clause(tbn_problem, sat_problem)

		while sat_problem.success:
			Encoder.increment_min_representatives(tbn_problem, sat_problem)
			sat_problem.solve()

		self.assertEqual(sat_problem.min_reps, 6)


if __name__ == '__main__':
	unittest.main()

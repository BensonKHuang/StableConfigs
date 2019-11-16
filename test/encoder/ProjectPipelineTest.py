import unittest
import stableconfigs.encoder.Encoder as Encoder
from stableconfigs.encoder.SATProblem import SATProblem
from stableconfigs.parser.Parser import parse_input_file


class SATSolverCase(unittest.TestCase):

	def test_basic(self):
		tbn_problem = parse_input_file("../../input/basic.txt")
		sat_problem = SATProblem()

		Encoder.encode_basic_clause(tbn_problem, sat_problem)

		while sat_problem.success:
			Encoder.increment_min_representatives(tbn_problem, sat_problem)
			sat_problem.solve()

		self.assertEquals(sat_problem.min_reps, 5)

	def test_and_gate(self):
		tbn_problem = parse_input_file("../../input/and_gate.txt")
		sat_problem = SATProblem()

		Encoder.encode_basic_clause(tbn_problem, sat_problem)

		while sat_problem.success:
			Encoder.increment_min_representatives(tbn_problem, sat_problem)
			sat_problem.solve()

		self.assertEquals(sat_problem.min_reps, 7)

	def test_wraparound_sorting_network(self):
		tbn_problem = parse_input_file("../../input/wraparound_sorting_network.txt")
		sat_problem = SATProblem()

		Encoder.encode_basic_clause(tbn_problem, sat_problem)

		while sat_problem.success:
			Encoder.increment_min_representatives(tbn_problem, sat_problem)
			sat_problem.solve()

		self.assertEquals(sat_problem.min_reps, 50)

	def test_strand_displacement(self):
		tbn_problem = parse_input_file("../../input/strand_displacement.txt")
		sat_problem = SATProblem()

		Encoder.encode_basic_clause(tbn_problem, sat_problem)

		while sat_problem.success:
			Encoder.increment_min_representatives(tbn_problem, sat_problem)
			sat_problem.solve()

		self.assertEquals(sat_problem.min_reps, 6)


if __name__ == '__main__':
	unittest.main()

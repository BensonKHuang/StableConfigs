import unittest
import stableconfigs

from stableconfigs.parser.Parser import parse_input_lines
from stableconfigs.encoder.SATProblem import SATProblem
from stableconfigs.common.CustomExceptions import *
from stableconfigs.encoder import Encoder
from stableconfigs.decoder import Decoder


class DecoderTest(unittest.TestCase):

    def setUp(self):
        self.monomer_input = ["a b",
                                "a* b*",
                                "a",
                                "b"]
        self.tbn_problem = parse_input_lines(self.monomer_input, [])
    
    def test_decoder_empty_result(self):
        sat_problem = SATProblem()
        polymers = Decoder.decode_boolean_values(self.tbn_problem, sat_problem)
        self.assertEqual(len(polymers), 0)
    
    def test_decoder_basic_1(self):
        sat_problem = SATProblem()
        Encoder.encode_basic_clause(self.tbn_problem, sat_problem)
        Encoder.increment_min_representatives(self.tbn_problem, sat_problem)
        sat_problem.solve()
        polymers = Decoder.decode_boolean_values(self.tbn_problem, sat_problem)
        self.assertEqual(len(polymers), 1)

    def test_decoder_basic_2(self):
        sat_problem = SATProblem()
        Encoder.encode_basic_clause(self.tbn_problem, sat_problem)
        Encoder.increment_min_representatives(self.tbn_problem, sat_problem)
        Encoder.increment_min_representatives(self.tbn_problem, sat_problem)

        sat_problem.solve()
        polymers = Decoder.decode_boolean_values(self.tbn_problem, sat_problem)
        self.assertEqual(len(polymers), 2)

    def test_decoder_basic_3(self):
        sat_problem = SATProblem()
        Encoder.encode_basic_clause(self.tbn_problem, sat_problem)
        Encoder.increment_min_representatives(self.tbn_problem, sat_problem)
        Encoder.increment_min_representatives(self.tbn_problem, sat_problem)
        Encoder.increment_min_representatives(self.tbn_problem, sat_problem)

        sat_problem.solve()
        polymers = Decoder.decode_boolean_values(self.tbn_problem, sat_problem)
        self.assertEqual(len(polymers), 3)

    def test_decoder_basic_no_result(self):
        sat_problem = SATProblem()
        Encoder.encode_basic_clause(self.tbn_problem, sat_problem)
        # Problem cannot decode into 4 polymers
        Encoder.increment_min_representatives(self.tbn_problem, sat_problem)
        Encoder.increment_min_representatives(self.tbn_problem, sat_problem)
        Encoder.increment_min_representatives(self.tbn_problem, sat_problem)
        Encoder.increment_min_representatives(self.tbn_problem, sat_problem)

        sat_problem.solve()
        polymers = Decoder.decode_boolean_values(self.tbn_problem, sat_problem)
        self.assertEqual(len(polymers), 0)


if __name__ == '__main__':
	unittest.main()

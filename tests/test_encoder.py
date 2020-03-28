import unittest
import stableconfigs

from stableconfigs.parser.Parser import parse_input_lines
from stableconfigs.encoder.SATProblem import SATProblem
from stableconfigs.common.CustomExceptions import *
from stableconfigs.encoder import Encoder


class EncoderTest(unittest.TestCase):

    def setUp(self):
        # And Gate monomer input
        self.monomer_input = ["a b c d e",
                              "a* b* c* d*",
                              "b* c*:s1 d* e*",
                              "d e f",
                              "a b >input1",
                              "b c:s2",
                              "c d:s3 >input2",
                              "e f >output",
                              "e* f*"]
        self.constraint_input = ["FREE output"]
        self.tbn_problem = parse_input_lines(
            self.monomer_input, self.constraint_input)

    def test_encode_each_site_binds_at_most_once(self):
        sat_problem = SATProblem()
        Encoder.encode_each_site_binds_at_most_once(
            self.tbn_problem, sat_problem)

        self.assertEqual(
            len(sat_problem.each_site_binds_at_most_once_clauses), 38)
        self.assertEqual(len(sat_problem.pair_to_id), 28)

    # Function requires previous pairs to be created
    def test_encode_limiting_site_binds(self):
        sat_problem = SATProblem()
        Encoder.encode_each_site_binds_at_most_once(
            self.tbn_problem, sat_problem)
        Encoder.encode_limiting_site_binds(
            self.tbn_problem, sat_problem)
        self.assertEqual(len(sat_problem.pair_to_id), 28)

        self.assertEqual(
            len(sat_problem.limited_site_binds_clauses), 10)
        self.assertTrue([1, 2] in sat_problem.limited_site_binds_clauses)
        self.assertTrue([3, 4, 5] in sat_problem.limited_site_binds_clauses)
        self.assertTrue([9, 10, 11] in sat_problem.limited_site_binds_clauses)
        self.assertTrue([12, 13, 14] in sat_problem.limited_site_binds_clauses)
        self.assertTrue([15, 16, 17] in sat_problem.limited_site_binds_clauses)
        self.assertTrue([18, 19, 20] in sat_problem.limited_site_binds_clauses)
        self.assertTrue([21, 22, 23] in sat_problem.limited_site_binds_clauses)
        self.assertTrue([24, 25, 26] in sat_problem.limited_site_binds_clauses)
        self.assertTrue([27, 28] in sat_problem.limited_site_binds_clauses)

    def test_encode_pair_implies_bind(self):
        sat_problem = SATProblem()
        Encoder.encode_each_site_binds_at_most_once(
            self.tbn_problem, sat_problem)
        Encoder.encode_limiting_site_binds(
            self.tbn_problem, sat_problem)
        Encoder.encode_pair_implies_bind(self.tbn_problem, sat_problem)

        self.assertEquals(len(sat_problem.bind_to_id), 14)
        # Same number as number of pairs!
        self.assertEquals(
            len(sat_problem.pair_implies_bind_clauses), len(sat_problem.pair_to_id))

    def test_encode_bind_transitive(self):
        sat_problem = SATProblem()
        Encoder.encode_each_site_binds_at_most_once(
            self.tbn_problem, sat_problem)
        Encoder.encode_limiting_site_binds(
            self.tbn_problem, sat_problem)
        Encoder.encode_pair_implies_bind(self.tbn_problem, sat_problem)
        Encoder.encode_bind_transitive(self.tbn_problem, sat_problem)

        self.assertEquals(len(sat_problem.bind_to_id), 36)
        self.assertEquals(
            len(sat_problem.bind_transitive_clauses), 252)

    def test_encode_bind_representatives(self):
        sat_problem = SATProblem()
        Encoder.encode_each_site_binds_at_most_once(
            self.tbn_problem, sat_problem)
        Encoder.encode_limiting_site_binds(
            self.tbn_problem, sat_problem)
        Encoder.encode_pair_implies_bind(self.tbn_problem, sat_problem)
        Encoder.encode_bind_transitive(self.tbn_problem, sat_problem)
        Encoder.encode_bind_representatives(self.tbn_problem, sat_problem)

        self.assertEquals(len(sat_problem.rep_to_id),
                          self.tbn_problem.monomer_count)
        self.assertEquals(len(sat_problem.bind_representatives_clauses), 36)

    def test_increment_min_representatives(self):
        sat_problem = SATProblem()
        Encoder.encode_basic_clause(self.tbn_problem, sat_problem)
        self.assertEqual(sat_problem.min_reps, 0)

        Encoder.increment_min_representatives(self.tbn_problem, sat_problem)
        self.assertEqual(sat_problem.min_reps, 1)
        self.assertEqual(
            len(sat_problem.increment_min_representatives_clauses), 10)

        Encoder.increment_min_representatives(self.tbn_problem, sat_problem)
        self.assertEqual(sat_problem.min_reps, 2)
        self.assertEqual(
            len(sat_problem.increment_min_representatives_clauses), 28)

        Encoder.increment_min_representatives(self.tbn_problem, sat_problem)
        self.assertEqual(sat_problem.min_reps, 3)
        self.assertEqual(
            len(sat_problem.increment_min_representatives_clauses), 45)

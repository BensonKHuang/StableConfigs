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
                              "e* f* >extra"]
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

        self.assertEqual(len(sat_problem.bind_to_id), 14)
        # Same number as number of pairs!
        self.assertEqual(
            len(sat_problem.pair_implies_bind_clauses), len(sat_problem.pair_to_id))

    def test_encode_bind_transitive(self):
        sat_problem = SATProblem()
        Encoder.encode_each_site_binds_at_most_once(
            self.tbn_problem, sat_problem)
        Encoder.encode_limiting_site_binds(
            self.tbn_problem, sat_problem)
        Encoder.encode_pair_implies_bind(self.tbn_problem, sat_problem)
        Encoder.encode_bind_transitive(self.tbn_problem, sat_problem)

        self.assertEqual(len(sat_problem.bind_to_id), 36)
        self.assertEqual(
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

        self.assertEqual(len(sat_problem.rep_to_id),
                         self.tbn_problem.monomer_count)
        self.assertEqual(len(sat_problem.bind_representatives_clauses), 36)

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

    # Constraint Encoder Tests
    def test_constraints_encoder_monomer_free(self):
        sat_problem = SATProblem()
        Encoder.encode_basic_clause(self.tbn_problem, sat_problem)
        Encoder.encode_constraints_clauses(self.tbn_problem, sat_problem)
        self.assertEqual(len(sat_problem.constraint_clauses), 8)
        for clause in sat_problem.constraint_clauses:
            self.assertEqual(len(clause), 1)

    def test_constraints_encoder_monomer_notfree(self):
        constraint_input = ["NOTFREE output"]
        tbn_problem = parse_input_lines(self.monomer_input, constraint_input)
        sat_problem = SATProblem()
        Encoder.encode_basic_clause(tbn_problem, sat_problem)
        Encoder.encode_constraints_clauses(tbn_problem, sat_problem)

        self.assertEqual(len(sat_problem.constraint_clauses), 1)
        self.assertEqual(len(sat_problem.constraint_clauses[0]), 8)

    def test_constraints_encoder_monomer_together(self):
        constraint_input = ["TOGETHER output extra"]
        tbn_problem = parse_input_lines(self.monomer_input, constraint_input)
        sat_problem = SATProblem()
        Encoder.encode_basic_clause(tbn_problem, sat_problem)
        Encoder.encode_constraints_clauses(tbn_problem, sat_problem)

        self.assertEqual(len(sat_problem.constraint_clauses), 1)
        self.assertEqual(len(sat_problem.constraint_clauses[0]), 1)

    def test_constraints_encoder_monomer_nottogether(self):
        constraint_input = ["NOTTOGETHER output extra"]
        tbn_problem = parse_input_lines(self.monomer_input, constraint_input)
        sat_problem = SATProblem()
        Encoder.encode_basic_clause(tbn_problem, sat_problem)
        Encoder.encode_constraints_clauses(tbn_problem, sat_problem)

        self.assertEqual(len(sat_problem.constraint_clauses), 1)
        self.assertEqual(len(sat_problem.constraint_clauses[0]), 1)
        self.assertLess(sat_problem.constraint_clauses[0][0], 0)

    def test_constraints_encoder_bsite_paired(self):
        constraint_input = ["PAIRED s1 s2"]
        tbn_problem = parse_input_lines(self.monomer_input, constraint_input)
        sat_problem = SATProblem()
        Encoder.encode_basic_clause(tbn_problem, sat_problem)
        Encoder.encode_constraints_clauses(tbn_problem, sat_problem)

        self.assertEqual(len(sat_problem.constraint_clauses), 1)
        self.assertEqual(len(sat_problem.constraint_clauses[0]), 1)
        pair_id = sat_problem.constraint_clauses[0][0]
        pair = sat_problem.id_to_pair.get(pair_id)
        self.assertEqual(pair.site1.name, "s1")
        self.assertEqual(pair.site2.name, "s2")

    def test_constraints_encoder_bsite_notpaired(self):
        constraint_input = ["NOTPAIRED s1 s2"]
        tbn_problem = parse_input_lines(self.monomer_input, constraint_input)
        sat_problem = SATProblem()
        Encoder.encode_basic_clause(tbn_problem, sat_problem)
        Encoder.encode_constraints_clauses(tbn_problem, sat_problem)

        self.assertEqual(len(sat_problem.constraint_clauses), 1)
        self.assertEqual(len(sat_problem.constraint_clauses[0]), 1)
        self.assertLess(sat_problem.constraint_clauses[0][0], 0)
        pair_id = -sat_problem.constraint_clauses[0][0]
        pair = sat_problem.id_to_pair.get(pair_id)
        self.assertEqual(pair.site1.name, "s1")
        self.assertEqual(pair.site2.name, "s2")

    def test_constraints_encoder_bsite_anypaired(self):
        constraint_input = ["ANYPAIRED s1"]
        tbn_problem = parse_input_lines(self.monomer_input, constraint_input)
        sat_problem = SATProblem()
        Encoder.encode_basic_clause(tbn_problem, sat_problem)
        Encoder.encode_constraints_clauses(tbn_problem, sat_problem)

        self.assertEqual(len(sat_problem.constraint_clauses), 1)
        num_complement = tbn_problem.site_type_to_sitelist_map.get(
            "c").get_normal_site_count()

        self.assertEqual(
            len(sat_problem.constraint_clauses[0]), num_complement)

    def test_constraints_encoder_bsite_notanypaired(self):
        constraint_input = ["NOTANYPAIRED s1"]
        tbn_problem = parse_input_lines(self.monomer_input, constraint_input)
        sat_problem = SATProblem()
        Encoder.encode_basic_clause(tbn_problem, sat_problem)
        Encoder.encode_constraints_clauses(tbn_problem, sat_problem)

        num_complement = tbn_problem.site_type_to_sitelist_map.get(
            "c").get_normal_site_count()
        self.assertEqual(len(sat_problem.constraint_clauses), num_complement)

    def test_constraints_encoder_together_constraint_exception(self):
        monomer_input = ["a >mon1",
                         "b >mon2"]
        constraint_input = ["TOGETHER mon1 mon2"]
        tbn_problem = parse_input_lines(monomer_input, constraint_input)
        sat_problem = SATProblem()
        Encoder.encode_basic_clause(tbn_problem, sat_problem)
        self.assertRaises(TogetherConstraintException,
                          Encoder.encode_constraints_clauses, tbn_problem, sat_problem)

    def test_constraints_encoder_not_free_constraint_exception(self):
        monomer_input = ["a >mon1",
                         "b >mon2"]
        constraint_input = ["NOTFREE mon1"]
        tbn_problem = parse_input_lines(monomer_input, constraint_input)
        sat_problem = SATProblem()
        Encoder.encode_basic_clause(tbn_problem, sat_problem)
        self.assertRaises(NotFreeConstraintException,
                          Encoder.encode_constraints_clauses, tbn_problem, sat_problem)

    def test_constraints_encoder_paired_constraint_exception(self):
        monomer_input = ["a:s1",
                         "b:s2"]
        constraint_input = ["PAIRED s1 s2"]
        tbn_problem = parse_input_lines(monomer_input, constraint_input)
        sat_problem = SATProblem()
        Encoder.encode_basic_clause(tbn_problem, sat_problem)
        self.assertRaises(PairedConstraintException,
                          Encoder.encode_constraints_clauses, tbn_problem, sat_problem)

    def test_constraints_encoder_any_paired_constraint_exception(self):
        monomer_input = ["a:s1",
                         "b:s2"]
        constraint_input = ["ANYPAIRED s1"]
        tbn_problem = parse_input_lines(monomer_input, constraint_input)
        sat_problem = SATProblem()
        Encoder.encode_basic_clause(tbn_problem, sat_problem)
        self.assertRaises(AnyPairedConstraintException,
                          Encoder.encode_constraints_clauses, tbn_problem, sat_problem)

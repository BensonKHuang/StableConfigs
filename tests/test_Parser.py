import unittest
import stableconfigs

from stableconfigs.parser.Parser import parse_input_lines
from stableconfigs.common.Constraint import CONSTR
from stableconfigs.common.CustomExceptions import *


class ParserTest(unittest.TestCase):

    def setUp(self):
        self.monomer_labeled = ["a:s1 b:s2 >mon1",
                                "a*:s3 b*:s4 >mon2",
                                "a*:s5 >mon3",
                                "b*:s6 >mon4"]

    def test_basic(self):
        monomer_basic = ["a b*",
                         "a* b",
                         "a",
                         "a* b",
                         "b",
                         "b"]
        tbn_problem = parse_input_lines(monomer_basic, [])

        # basic count check
        self.assertEqual(tbn_problem.monomer_count, 6)
        self.assertEqual(len(tbn_problem.all_monomers), 6)
        self.assertEqual(tbn_problem.site_count, 9)

        # check if valid number of non-complements and complements
        site_list_a = tbn_problem.site_type_to_sitelist_map.get("a")
        site_list_b = tbn_problem.site_type_to_sitelist_map.get("b")

        self.assertEqual(len(site_list_a._complementary_sites), 2)
        self.assertEqual(len(site_list_b._complementary_sites), 1)

    def test_no_b_complement(self):
        monomer_tiny = ["a b",
                        "a*"]
        tbn_problem = parse_input_lines(monomer_tiny, [])

        # basic count check
        self.assertEqual(tbn_problem.monomer_count, 2)
        self.assertEqual(len(tbn_problem.all_monomers), 2)
        self.assertEqual(tbn_problem.site_count, 3)

        # check a 0-complement problem
        site_list_a = tbn_problem.site_type_to_sitelist_map.get("a")
        site_list_b = tbn_problem.site_type_to_sitelist_map.get("b")

        self.assertEqual(len(site_list_a._complementary_sites), 1)
        self.assertEqual(len(site_list_b._complementary_sites), 0)

    def test_one_site(self):
        monomer_onesite = ["a",
                           "a*",
                           "a",
                           "a*"]
        tbn_problem = parse_input_lines(monomer_onesite, [])

        # basic count check
        self.assertEqual(tbn_problem.monomer_count, 4)
        self.assertEqual(len(tbn_problem.all_monomers), 4)
        self.assertEqual(tbn_problem.site_count, 4)

        # check a single site problem instance
        site_list_a = tbn_problem.site_type_to_sitelist_map.get("a")
        site_list_b = tbn_problem.site_type_to_sitelist_map.get("b")

        self.assertEqual(len(site_list_a._complementary_sites), 2)
        self.assertEqual(site_list_b, None)

    def test_comment(self):
        monomer_comment_url = "../input/comment.txt"
        tbn_file = open(monomer_comment_url, 'rt')
        monomer_comment = tbn_file.readlines()
        tbn_file.close()

        tbn_problem = parse_input_lines(monomer_comment, [])

        self.assertEqual(tbn_problem.monomer_count, 4)
        self.assertEqual(len(tbn_problem.all_monomers), 4)
        self.assertEqual(tbn_problem.site_count, 6)

        site_list_c = tbn_problem.site_type_to_sitelist_map.get("c")

        self.assertEqual("c" in tbn_problem.site_type_to_sitelist_map.keys(),  False)

    def test_and_gate_parsing(self):
        monomer_and_gate_url = "../input/and_gate.txt"
        tbn_file = open(monomer_and_gate_url, 'rt')
        monomer_and_gate = tbn_file.readlines()
        tbn_file.close()

        tbn_problem = parse_input_lines(monomer_and_gate, [])

        self.assertEqual(tbn_problem.monomer_count, 9)
        self.assertEqual(len(tbn_problem.all_monomers), 9)
        self.assertEqual(tbn_problem.site_count, 26)

        site_list_e = tbn_problem.site_type_to_sitelist_map.get("e")
        site_list_f = tbn_problem.site_type_to_sitelist_map.get("f")

        self.assertEqual(len(site_list_e._complementary_sites), 2)
        self.assertEqual(len(site_list_f._complementary_sites), 1)

    def test_and_gate_names(self):
        monomer_and_gate_url = "../input/and_gate.txt"
        tbn_file = open(monomer_and_gate_url, 'rt')
        monomer_and_gate = tbn_file.readlines()
        tbn_file.close()

        tbn_problem = parse_input_lines(monomer_and_gate, [])

        # Verify Binding Site Names
        self.assertEqual(len(tbn_problem.bindingsite_name_map), 3)

        bsite_1 = tbn_problem.bindingsite_name_map.get("s1")
        self.assertEqual(bsite_1.name, "s1")
        self.assertEqual(bsite_1.type, "c")
        self.assertEqual(bsite_1.IsComplement, True)

        bsite_2 = tbn_problem.bindingsite_name_map.get("s2")
        self.assertEqual(bsite_2.name, "s2")
        self.assertEqual(bsite_2.type, "c")
        self.assertEqual(bsite_2.IsComplement, False)

        bsite_3 = tbn_problem.bindingsite_name_map.get("s3")
        self.assertEqual(bsite_3.name, "s3")
        self.assertEqual(bsite_3.type, "d")
        self.assertEqual(bsite_3.IsComplement, False)

        # Verify Monomer Names
        input_1 = tbn_problem.monomer_name_map.get("input1")
        self.assertEqual(input_1.name, "input1")
        self.assertEqual(len(input_1.BindingSites), 2)

        input_2 = tbn_problem.monomer_name_map.get("input2")
        self.assertEqual(input_2.name, "input2")
        self.assertEqual(len(input_2.BindingSites), 2)

        output = tbn_problem.monomer_name_map.get("output")
        self.assertEqual(output.name, "output")
        self.assertEqual(len(output.BindingSites), 2)

    # Testing constraints for monomers
    def test_constraint_monomer_free(self):
        constr_input = ["FREE mon1"]
        tbn_problem = parse_input_lines(self.monomer_labeled, constr_input)
        constr = tbn_problem.constraints[0]
        self.assertEqual(constr.c_type, CONSTR.FREE)
        self.assertEqual(len(constr.arguments), 1)

    def test_constraint_monomer_notfree(self):
        constr_input = ["NOTFREE mon1"]
        tbn_problem = parse_input_lines(self.monomer_labeled, constr_input)
        constr = tbn_problem.constraints[0]
        self.assertEqual(constr.c_type, CONSTR.NOTFREE)
        self.assertEqual(len(constr.arguments), 1)

    def test_constraint_monomer_together(self):
        constr_input = ["TOGETHER mon1 mon2"]
        tbn_problem = parse_input_lines(self.monomer_labeled, constr_input)
        constr = tbn_problem.constraints[0]
        self.assertEqual(constr.c_type, CONSTR.TOGETHER)
        self.assertEqual(len(constr.arguments), 2)

    def test_constraint_monomer_nottogether(self):
        constr_input = ["NOTTOGETHER mon1 mon2"]
        tbn_problem = parse_input_lines(self.monomer_labeled, constr_input)
        constr = tbn_problem.constraints[0]
        self.assertEqual(constr.c_type, CONSTR.NOTTOGETHER)
        self.assertEqual(len(constr.arguments), 2)

    # Testing Constraints for Binding Sites
    def test_constraint_bsite_paired(self):
        constr_input = ["PAIRED s1 s3"]
        tbn_problem = parse_input_lines(self.monomer_labeled, constr_input)
        constr = tbn_problem.constraints[0]
        self.assertEqual(constr.c_type, CONSTR.PAIRED)
        self.assertEqual(len(constr.arguments), 2)

    def test_constraint_bsite_notpaired(self):
        constr_input = ["NOTPAIRED s1 s3"]
        tbn_problem = parse_input_lines(self.monomer_labeled, constr_input)
        constr = tbn_problem.constraints[0]
        self.assertEqual(constr.c_type, CONSTR.NOTPAIRED)
        self.assertEqual(len(constr.arguments), 2)

    def test_constraint_bsite_anypaired(self):
        constr_input = ["ANYPAIRED s1"]
        tbn_problem = parse_input_lines(self.monomer_labeled, constr_input)
        constr = tbn_problem.constraints[0]
        self.assertEqual(constr.c_type, CONSTR.ANYPAIRED)
        self.assertEqual(len(constr.arguments), 1)

    def test_constraint_bsite_notanypaired(self):
        constr_input = ["NOTANYPAIRED s1"]
        tbn_problem = parse_input_lines(self.monomer_labeled, constr_input)
        constr = tbn_problem.constraints[0]
        self.assertEqual(constr.c_type, CONSTR.NOTANYPAIRED)
        self.assertEqual(len(constr.arguments), 1)

    # Exception Handling
    def test_empty_problem_exception(self):
        self.assertRaises(EmptyProblemException, parse_input_lines, [], [])

    # Parsing Exception Handling
    def test_duplicate_monomer_name_exception(self):
        monomer_input = ["a >mon1",
                         "b >mon1"]
        self.assertRaises(DuplicateMonomerNameException,
                          parse_input_lines, monomer_input, [])

    def test_duplicate_bsite_name_exception(self):
        monomer_input = ["a:s1",
                         "b:s1"]
        self.assertRaises(DuplicateBindingSiteNameException,
                          parse_input_lines, monomer_input, [])

    # Constraints Parsing Exception Handling
    def test_invalid_monomer_name_exception(self):
        monomer_input = ["a >"]
        self.assertRaises(EmptyMonomerNameException,
                          parse_input_lines, monomer_input, [])

    def test_invalid_bsite_name_exception(self):
        monomer_input = ["a:"]
        self.assertRaises(InvalidBindingSiteNameException,
                          parse_input_lines, monomer_input, [])

    def test_invalid_bsite_name_exception_2(self):
        monomer_input = ["*"]
        self.assertRaises(InvalidBindingSiteNameException,
                          parse_input_lines, monomer_input, [])
    
    def test_invalid_bsite_name_exception_3(self):
        monomer_input = [":s1"]
        self.assertRaises(InvalidBindingSiteNameException,
                          parse_input_lines, monomer_input, [])

    def test_nonexistent_monomer_exception(self):
        monomer_input = ["a"]
        constraint_input = ["FREE mon1"]
        self.assertRaises(NonexistentMonomerException,
                          parse_input_lines, monomer_input, constraint_input)

    def test_nonexistent_bsite_exception(self):
        monomer_input = ["a"]
        constraint_input = ["ANYPAIRED s1"]
        self.assertRaises(NonexistentBindingSiteException,
                          parse_input_lines, monomer_input, constraint_input)

    def test_constraint_argument_count_exception(self):
        monomer_input = ["a:s1 a*:s2"]
        constraint_input = ["ANYPAIRED s1 s2"]
        self.assertRaises(ConstraintArgumentCountException,
                          parse_input_lines, monomer_input, constraint_input)

    def test_invalid_constraint_exception(self):
        monomer_input = ["a"]
        constraint_input = ["BADCONSTRAINT"]
        self.assertRaises(InvalidConstraintException,
                          parse_input_lines, monomer_input, constraint_input)


if __name__ == '__main__':
	unittest.main()

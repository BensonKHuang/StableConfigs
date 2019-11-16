import unittest
from stableconfigs.parser.Parser import parse_input_file


class ParserTest(unittest.TestCase):
    def test_basic(self):
        tbn_problem = parse_input_file("../../input/basic.txt")

        # basic count check
        self.assertEqual(tbn_problem.monomer_count, 6)
        self.assertEqual(len(tbn_problem.all_monomers), 6)
        self.assertEqual(tbn_problem.site_count, 9)

        # check if valid number of non-complements and complements
        site_list_a = tbn_problem.site_name_to_sitelist_map.get("a")
        site_list_b = tbn_problem.site_name_to_sitelist_map.get("b")

        self.assertEqual(len(site_list_a._complementary_sites), 2)
        self.assertEqual(len(site_list_b._complementary_sites), 1)

    def test_no_b_complement(self):
        tbn_problem = parse_input_file("../../input/tiny.txt")

        # basic count check
        self.assertEqual(tbn_problem.monomer_count, 2)
        self.assertEqual(len(tbn_problem.all_monomers), 2)
        self.assertEqual(tbn_problem.site_count, 3)

        # check a 0-complement problem
        site_list_a = tbn_problem.site_name_to_sitelist_map.get("a")
        site_list_b = tbn_problem.site_name_to_sitelist_map.get("b")

        self.assertEqual(len(site_list_a._complementary_sites), 1)
        self.assertEqual(len(site_list_b._complementary_sites), 0)

    def test_one_site(self):
        tbn_problem = parse_input_file("../../input/one_site.txt")

        # basic count check
        self.assertEqual(tbn_problem.monomer_count, 4)
        self.assertEqual(len(tbn_problem.all_monomers), 4)
        self.assertEqual(tbn_problem.site_count, 4)

        # check a single site problem instance
        site_list_a = tbn_problem.site_name_to_sitelist_map.get("a")
        site_list_b = tbn_problem.site_name_to_sitelist_map.get("b")

        self.assertEqual(len(site_list_a._complementary_sites), 2)
        self.assertEqual(site_list_b, None)

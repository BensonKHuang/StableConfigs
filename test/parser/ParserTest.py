import unittest
from src.parser.Parser import parse_input_file


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

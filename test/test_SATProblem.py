import unittest
from stableconfigs.encoder.SATProblem import SATProblem


class Test_SATProblem(unittest.TestCase):
    def test_solve_empty_clause(self):
        sat_problem = SATProblem()
        sat_problem.add_clause([])
        sat_problem.solve()
        success = sat_problem.success
        result = sat_problem.result

        self.assertFalse(success)
        self.assertEqual(0, len(result))
        self.assertEqual([], result)

    def test_solve_single_clause(self):
        sat_problem = SATProblem()
        sat_problem.add_clause([1])
        sat_problem.solve()
        success = sat_problem.success
        result = sat_problem.result

        self.assertTrue(success)
        self.assertEqual(1, len(result))
        self.assertEqual([1], result)

    def test_solve_basic_clauses(self):
        sat_problem = SATProblem()
        sat_problem.add_clause([1, 2, 3])
        sat_problem.add_clause([-2])
        sat_problem.add_clause([-3])
        sat_problem.solve()
        success = sat_problem.success
        result = sat_problem.result

        self.assertTrue(success)
        self.assertEqual(3, len(result))
        self.assertEqual([1, -2, -3], result)

    def test_solve_conflicting_clauses(self):
        sat_problem = SATProblem()
        sat_problem.add_clause([1, 2])
        sat_problem.add_clause([-1])
        sat_problem.add_clause([-2])
        sat_problem.solve()
        success = sat_problem.success
        result = sat_problem.result

        self.assertFalse(success)
        self.assertEqual(0, len(result))
        self.assertEqual([], result)

    def test_solve_basic_clauses_2(self):
        sat_problem = SATProblem()
        sat_problem.add_clause([-1, -3, -4])
        sat_problem.add_clause([2, 3, -4])
        sat_problem.add_clause([1, -2, 4])
        sat_problem.add_clause([1, 3, 4])
        sat_problem.add_clause([-1, 2, -3])
        sat_problem.add_clause([2])
        sat_problem.solve()
        success = sat_problem.success
        result = sat_problem.result

        self.assertTrue(success)
        self.assertEqual(4, len(result))
        self.assertEqual([1, 2, -3, -4], result)


if __name__ == '__main__':
    unittest.main()

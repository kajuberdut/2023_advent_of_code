import unittest

from aoc.day6 import solution


class TestDay1Function(unittest.TestCase):
    def test_first_solution(self):
        expected = 32076
        self.assertEqual(solution.solve1(), expected, f"Should be {expected}")

    def test_second_solution(self):
        expected = 34278221
        self.assertEqual(solution.solve2(), expected, f"Should be {expected}")


# This allows running the tests from the command line
if __name__ == "__main__":
    unittest.main()

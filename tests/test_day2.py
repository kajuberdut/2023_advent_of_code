import unittest

from aoc.day2 import solution
from collections import defaultdict


class TestDay1Function(unittest.TestCase):
    test_line = "Game 75: 4 blue; 4 green, 6 blue; 2 green, 2 blue, 4 red"

    # Test method must start with 'test'
    def test_parse(self):
        parsed_data = solution.parse_line(self.test_line)
        self.assertEqual(parsed_data[0], 75)
        self.assertEqual(
            parsed_data[1], {"blue": [4, 6, 2], "green": [4, 2], "red": [4]}
        )

    def test_handle_line_fail(self):
        id1 = solution.id_if_possible(self.test_line, {})
        self.assertEqual(id1, 0)

    def test_handle_line_pass(self):
        id2 = solution.id_if_possible(
            self.test_line, {color: 100 for color in ["red", "green", "blue"]}
        )
        self.assertEqual(id2, 75)

    def test_first_solution(self):
        expected = 1867
        self.assertEqual(
            solution.solve1(solution.FIRST_TEST), expected, f"Should be {expected}"
        )

    def test_power_of_line(self):
        pow = solution.power_of_line(self.test_line)
        self.assertEqual(pow, 96)

    def test_second_solution(self):
        expected = 84538
        self.assertEqual(solution.solve2(), expected, f"should be {expected}")


# This allows running the tests from the command line
if __name__ == "__main__":
    unittest.main()

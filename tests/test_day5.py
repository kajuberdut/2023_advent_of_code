import unittest

from aoc.day5 import part_one, part_two


class TestDay1Function(unittest.TestCase):
    def test_first_solution(self):
        expected = 525792406
        self.assertEqual(part_one.solve1(), expected, f"Should be {expected}")

    def test_second_solution(self):
        expected = 79004094
        self.assertEqual(part_two.solve2(), expected, f"Should be {expected}")


# This allows running the tests from the command line
if __name__ == "__main__":
    unittest.main()

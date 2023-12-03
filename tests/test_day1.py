import unittest

from aoc.day1 import solution

class TestDay1Function(unittest.TestCase):

    # Test method must start with 'test'
    def test_first_part(self):
        expected = 55090
        # Empty dict for digits means no strings will be interpreted as digits
        self.assertEqual(solution.solve(digits={}), expected, f"Should be {expected}")

    def test_second_part(self):
        expected = 54845
        self.assertEqual(solution.solve(), expected, f"Should be {expected}")

# This allows running the tests from the command line
if __name__ == '__main__':
    unittest.main()

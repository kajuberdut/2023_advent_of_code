import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='Run Advent of Code solutions.')
    parser.add_argument('day', type=int, help='The day of the solution to run (e.g., 1 for Day 1)')

    # Parse the arguments
    args = parser.parse_args()

    # Dynamically import the solution module for the given day
    try:
        day_module = __import__(f'aoc.day{args.day}.solution', fromlist=['main'])
        day_module.main()
    except ModuleNotFoundError:
        print(f'Solution for day {args.day} not found.')
        sys.exit(1)
    except AttributeError:
        print(f'Module for day {args.day} does not have a "main" function.')
        sys.exit(1)

if __name__ == '__main__':
    main()

import re
from collections import defaultdict

from aoc.utility import load_input

FIRST_TEST = {"red": 12, "green": 13, "blue": 14}

# Pattern to capture the game number and all rgb-quantity pairs
GAME_PATTERN = r"Game (?P<game_number>\d+):"
RGB_PATTERN = r"(\d+) (green|blue|red)"


def parse_line(game_string) -> tuple[int, dict]:
    # Find the game number
    game_number_match = re.search(GAME_PATTERN, game_string)
    if not game_number_match:
        return None

    game_number = int(game_number_match.group("game_number"))

    game_info = defaultdict(list)

    # Find all rgb-quantity pairs
    rgb_quantity_matches = re.findall(RGB_PATTERN, game_string)
    for quantity, rgb in rgb_quantity_matches:
        game_info[rgb].append(int(quantity))

    return game_number, game_info


def id_if_possible(line: str, possible_rgb: dict) -> bool:
    id, seen_rgb = parse_line(line)
    for rgb in seen_rgb.keys():
        possible = possible_rgb.get(rgb)
        seen = seen_rgb[rgb]
        if seen and not possible:
            return 0
        for q in seen:
            if q > possible:
                return 0
    return id

def solve1(possible_rgb: dict):
    lines = load_input(__file__).splitlines()
    passing_ids = [id_if_possible(line, possible_rgb) for line in lines]
    return sum(passing_ids)

def power_of_line(line: str) -> int:
    id, seen_rgb = parse_line(line)
    a, b, c = [max(cubes) for cubes in seen_rgb.values()]
    return a * b * c

def solve2():
    lines = load_input(__file__).splitlines()
    return sum([power_of_line(line) for line in lines])

def main():
    
    result_part_1 = solve1(FIRST_TEST)
    result_part_2 = solve2()
    print(f"{result_part_1=}, {result_part_2=}")

if __name__ == "__main__":
    main()

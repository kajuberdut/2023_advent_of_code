import multiprocessing
import re
from collections import defaultdict

from aoc.utility import load_input

A_TO_B_PATERN = r"(\w+)-to-(\w+) map:"
num_processes = multiprocessing.cpu_count()


class Maps:
    def __init__(self):
        self.data = defaultdict(list)
        self.current_key = None

    @classmethod
    def from_lines(cls, lines: list) -> "Maps":
        lines = [line for line in lines if line.strip()]

        m = cls()
        for line in lines:
            if " map:" in line:
                m.set_current(line)
            else:
                m.row(line)
        return m

    @classmethod
    def extract_a_b(self, map_string: str) -> tuple:
        matches = re.findall(A_TO_B_PATERN, map_string)
        return matches[0]

    def set_current(self, map_row: str):
        self.current_key = self.extract_a_b(map_row)

    def row(self, row_text: str):
        b, a, delta = [int(v) for v in row_text.split()]

        row_data = {
            "range": range(a, a + delta),
            "offset": b - a,
        }
        self.data[self.current_key].append(row_data)

    def find_key(self, target: str):
        return next(key for key in self.data.keys() if key[0] == target)

    def resolve_id(self, in_id: int) -> int:
        target = "seed"
        value = in_id

        while target and target != "location":
            key = self.find_key(target=target)
            values = self.data[key]

            try:
                result = next(v for v in values if value in v["range"])
                value += result["offset"]
            except StopIteration:
                # value stays the same if no mapping.
                pass

            target = key[1]

        return value


def solve1():
    raw_lines = load_input(__file__).splitlines()
    seeds = [int(seed) for seed in raw_lines.pop(0).split(":")[1].split()]

    m = Maps.from_lines(raw_lines)

    result = [m.resolve_id(seed) for seed in seeds]

    return min(result)

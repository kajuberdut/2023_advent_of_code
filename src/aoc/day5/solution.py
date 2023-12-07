import multiprocessing
import re
from collections import defaultdict

from aoc.utility import load_input, split_range_into_n

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
    
    def resolve_id_range(self, in_id: int) -> int:
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


def worker(block, seed_ranges, resolve_id_func):
    for location_id in block:
        seed_id = resolve_id_func(location_id)
        if any(sr for sr in seed_ranges if seed_id in sr):
            return location_id
    return None


def solve2():
    raw_lines = load_input(__file__).splitlines()
    seed_line = [int(seed) for seed in raw_lines.pop(0).split(":")[1].split()]
    seed_pairs = zip(seed_line[::2], seed_line[1::2])
    seed_ranges = [range(start, start + length) for start, length in seed_pairs]

    m = Maps.from_lines(raw_lines)
    least = 99999999999

    # Work through one block of locations at at time
    for ran in seed_ranges:
        for block in split_range_into_n(ran, 100):
            print(f"solving {block=}")
            chunk_size = len(block) // num_processes
            chunks = [
                block[i : i + chunk_size] for i in range(0, len(block), chunk_size)
            ]
            with multiprocessing.Pool(processes=num_processes) as pool:
                results = pool.starmap(
                    worker, [(chunk, seed_ranges, m.resolve_id) for chunk in chunks]
                )

            least = min([least, *[result for result in results if result is not None]])
            print(f"{least=}")
    return least


def main():
    result_part_1 = solve1()
    result_part_2 = solve2()
    print(f"{result_part_1=}, {result_part_2=}")


if __name__ == "__main__":
    main()

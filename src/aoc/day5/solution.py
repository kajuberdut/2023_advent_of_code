import re
import sqlite3

from aoc.database import DB, execute_statements, insert_many, query
from aoc.utility import load_input

A_TO_B_PATERN = r"(\w+)-to-(\w+) map:"
DB.connect(":memory:")


class Maps:
    def __init__(self):
        self.data = []
        self.current_source = None
        self.current_destination = None

    @classmethod
    def from_lines(cls, lines: list) -> "Maps":
        lines = [line for line in lines if line.strip()]

        m = cls()
        for line in lines:
            if " map:" in line:
                m.set_current(line)
            else:
                m.row(line)

        m.populate_db()
        return m

    def populate_db(self):
        create_sql = """
        CREATE TABLE IF NOT EXISTS maps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source              TEXT,
            source_start        INTEGER,
            source_end          INTEGER,
            destination         TEXT,
            destination_start   INTEGER,
            offset              INTEGER,
            UNIQUE(source, source_start) ON CONFLICT IGNORE
        );
        """
        execute_statements(create_sql)
        insert_many(table_name="maps", data=self.data)

    @classmethod
    def extract_a_b(self, map_string: str) -> tuple:
        matches = re.findall(A_TO_B_PATERN, map_string)
        return matches[0] if matches else ()

    def set_current(self, map_row: str):
        self.current_source, self.current_destination = self.extract_a_b(map_row)

    def row(self, row_text: str):
        b, a, delta = [int(v) for v in row_text.split()]
        row_data = {
            "source": self.current_source,
            "source_start": a,
            "source_end": a + delta - 1,
            "destination": self.current_destination,
            "destination_start": b,
            "offset": delta,
        }
        self.data.append(row_data)

    def resolve_seed(self, seed_id: int) -> int:
        source = "seed"
        value = seed_id

        while source and source != "location":
            maps_query = f"""
            SELECT destination
                ,  {value} + (destination_start - source_start)
                AS destination_id
                , source_start
                , destination_start
            FROM maps
            WHERE source = '{source}'
            AND {value} between source_start AND source_end
            """
            result = query(query=maps_query)
            if len(result) > 1:
                raise ValueError(f"Too many results: {result}")
            if result:
                source, value, *_ = result[0]
            else:
                destination_query = f"""
                    SELECT DISTINCT destination 
                    FROM maps 
                    WHERE source = '{source}'
                    """

                # value stays the same if no mapping.
                source = query(query=destination_query, exactly_one=True)[0][0]

        return value


def solve1():
    raw_lines = load_input(__file__).splitlines()
    seeds = [int(seed) for seed in raw_lines.pop(0).split(":")[1].split()]

    m = Maps.from_lines(raw_lines)

    result = [m.resolve_seed(seed) for seed in seeds]

    return min(result)


def solve2():
    raw_lines = load_input(__file__).splitlines()
    seed_ranges = [int(seed) for seed in raw_lines.pop(0).split(":")[1].split()]
    seed_pairs = zip(seed_ranges[::2], seed_ranges[1::2])

    m = Maps.from_lines(raw_lines)

    least = None

    # for start, length in seed_pairs:
    #     result = min(m.resolve_seed(start + delta) for delta in range(length))
    #     if result < least or result is None:
    #         least = result

    return least


def main():
    result_part_1 = solve1()
    result_part_2 = solve2()
    print(f"{result_part_1=}, {result_part_2=}")


if __name__ == "__main__":
    main()

import dataclasses
from collections import defaultdict
from functools import partial

from aoc.utility import load_input

default_list_dict = partial(defaultdict, list)


class Map:
    """Borg pattern collection of Lines."""

    _map: dict[int, "Line"] = {}

    @classmethod
    def get(cls, i):
        try:
            return cls._map[i]
        except KeyError:
            return Line()

    @classmethod
    def check_symbol(cls, i: int, locations: set[int], number: "Number") -> bool:
        line = cls.get(i)
        hits = list(locations & line.symbols)
        for hit in hits:
            line.symbol_hits[hit].append(number)
        return bool(hits)


@dataclasses.dataclass
class Number:
    line: "Line"
    value: int = 0
    location: set = dataclasses.field(default_factory=set)

    def __iadd__(self, other):
        self.value = int(f"{self.value}{other}")
        return self

    @property
    def padded(self):
        padded = self.location.copy()
        padded.add(min(self.location) - 1)
        padded.add(max(self.location) + 1)
        return padded

    def check_symbol(self, i, locations: set[int]):
        return Map.check_symbol(i, locations, self)

    def validated(self) -> int:
        i = self.line.line_number
        padded = self.padded

        # case 1: symbol to the right or left
        if self.check_symbol(i, set([min(padded), max(padded)])):
            return self.value
        # case 2: line above
        if self.check_symbol(i - 1, padded):
            return self.value
        # case 2: line below
        if self.check_symbol(i + 1, padded):
            return self.value
        # otherwise 0
        return 0


@dataclasses.dataclass
class Line:
    line_number: int = None
    symbols: set[int] = dataclasses.field(default_factory=set)
    numbers: list[Number] = dataclasses.field(default_factory=list)
    symbol_hits: dict[int, list] = dataclasses.field(default_factory=default_list_dict)

    def __post_init__(self):
        if self.line_number is not None:
            Map._map[self.line_number] = self

    @classmethod
    def from_str(
        cls, line_number: int, string: str, valid_symbol: str | None = None
    ) -> "Line":
        line = cls(line_number)

        current_number = Number(line)

        for index, char in enumerate(string):
            if char.isdigit():
                # Add index to current number
                current_number.location.add(index)
                current_number += char
            else:
                # If the current character is not a digit, check if we have a number
                if current_number.value:
                    line.numbers.append(current_number)
                    current_number = Number(line)

                # Add non-period symbols to the symbols list
                if char != ".":
                    if valid_symbol is None or char == valid_symbol:
                        line.symbols.add(index)

        # Save remaining number
        if current_number.value:
            line.numbers.append(current_number)

        return line

    def number_total(self):
        return sum([number.validated() for number in self.numbers])

    def ratio_total(self):
        total = 0
        for hits in self.symbol_hits.values():
            if len(hits) == 2:
                total += hits[0].value * hits[1].value
        return total


def solve1():
    lines = load_input(__file__).splitlines()
    result = sum(
        [
            line.number_total()
            for line in [Line.from_str(i, line) for i, line in enumerate(lines)]
        ]
    )
    return result


def solve2():
    text_lines = load_input(__file__).splitlines()
    lines = [Line.from_str(i, line) for i, line in enumerate(text_lines)]
    _ = [line.number_total() for line in lines]
    result = sum([line.ratio_total() for line in lines])
    return result


def main():
    result_part_1 = solve1()
    result_part_2 = solve2()
    print(f"{result_part_1=}, {result_part_2=}")


if __name__ == "__main__":
    main()

import itertools
import re

from aoc.utility import load_input

def build_digit_dict():
    # Mapping English names of digits to their numerical representations.
    # This is needed because some digits in the calibration document are spelled out.
    digit_names = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    digits = {name: str(i + 1) for i, name in enumerate(digit_names)}

    # Handling cases where spelled-out digits overlap in the calibration document.
    # E.G 'oneight' should be interpreted as '1' or '8' but a simple regex
    #  for number names will always find 1.
    # The overlapping dictionary maps these cases to tuples representing their numeric values
    # for first or last match as in {"oneight": (1, 8)}.
    overlapping = {
        f"{a}{b[1:]}": (str(digits[a]), str(digits[b]))
        for a, b in itertools.product(digit_names, digit_names)
        if a[-1] == b[0]  # Check for overlapping last and first letters.
    }
    # Merging overlapping cases with the original digits dictionary.
    digits = {**overlapping, **digits}

    return digits



def solve(digits: dict | None = None) -> int:

    if digits is None:
        digits = build_digit_dict()

    # Regular expression pattern to match numeric digits and spelled-out digit names.
    PATTERN = "|".join([*["\d"], *digits.keys()])


    def resolve_value(value: tuple | str, index=0):
        # If the value is a tuple (due to overlapping digits), it selects the appropriate part.
        result = digits.get(value, value)
        if isinstance(result, tuple):
            return result[index]
        return result


    def resolve_line(text_line: str) -> int:
        # Extracts and resolves the first and last digits from a line of text.
        found = re.findall(PATTERN, text_line)
        first, last = resolve_value(found[0]), resolve_value(found[-1], 1)
        return int(f"{first}{last}")


    # Reading the calibration document and computing the sum of calibration values.
    values = [
        resolve_line(row) for row in load_input(__file__, "calibration.txt").splitlines()
    ]

    # Summing up the calibration values to get the final result.
    result = sum(values)

    return result

def main():
    result_part_1 = solve({})
    result_part_2 = solve()
    print(f"{result_part_1=}, {result_part_2=}")

if __name__ == "__main__":
    main()
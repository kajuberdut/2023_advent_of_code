import re
import pathlib
import itertools

# Use an empty dict for digits to get the first solution.
digit_names = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
digits = {name: str(i + 1) for i, name in enumerate(digit_names)}
overlapping = {
    f"{a}{b[1:]}": (str(digits[a]), str(digits[b]))
    for a, b in itertools.product(digit_names, digit_names)
    if a[-1] == b[0]
}
digits = {**overlapping, **digits}

PATTERN = "\d" + "|" + "|".join(digits.keys())


def resolve_value(value: tuple | str, index=0):
    result = digits.get(value, value)
    if isinstance(result, tuple):
        return result[index]
    return result


def resolve_line(text_line: str) -> int:
    found = re.findall(PATTERN, text_line)
    first, last = resolve_value(found[0]), resolve_value(found[-1], 1)
    return int(f"{first}{last}")


values = [
    resolve_line(row)
    for row in (pathlib.Path(__file__).parent / "in.txt")
    .read_text(encoding="utf-8")
    .splitlines()
]

result = sum(values)

print(result)

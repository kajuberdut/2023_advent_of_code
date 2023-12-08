import pathlib


def load_input(dir: pathlib.Path | str, file_name: str = "input.txt"):
    dir = pathlib.Path(dir)
    if dir.is_file():
        dir = dir.parent
    return (dir / file_name).read_text(encoding="utf-8")


def split_range(original_range, n=2):
    total_length = len(original_range)
    n_length = total_length // n

    new_ranges = []
    for i in range(n):
        start = original_range.start + i * n_length
        end = start + n_length
        if i == n - 1:  # To handle the last quarter correctly
            end = original_range.stop
        new_ranges.append(range(start, end))

    return new_ranges


def bump_range(r: range, n: int) -> range:
    return range(r.start + n, r.stop + n)

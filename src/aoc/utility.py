import pathlib


def load_input(dir: pathlib.Path | str, file_name: str = "input.txt"):
    dir = pathlib.Path(dir)
    if dir.is_file():
        dir = dir.parent
    return (dir / file_name).read_text(encoding="utf-8")


def split_range_into_n(original_range, n=4):
    total_length = len(original_range)
    n_length = total_length // n

    new_ranges = []
    for i in range(n):
        start = original_range.start + i * n_length
        end = start + n_length
        if i == n-1:  # To handle the last quarter correctly
            end = original_range.stop
        new_ranges.append(range(start, end))

    return new_ranges

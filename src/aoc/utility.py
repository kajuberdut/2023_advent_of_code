import pathlib


def load_input(dir: pathlib.Path | str, file_name: str = "input.txt"):
    dir = pathlib.Path(dir)
    if dir.is_file():
        dir = dir.parent
    return (dir / file_name).read_text(encoding="utf-8")

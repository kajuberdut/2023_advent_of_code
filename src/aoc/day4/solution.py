from aoc.utility import load_input


def solve_line(line: str) -> tuple[str, str]:
    winning, have = line.split("|")
    winning = set(winning.split(":")[1].split())
    have = set(have.split())
    return len(winning & have)


def solve1():
    rewards = [1]
    [rewards.append(rewards[-1] * 2) for _ in range(25)]

    text_lines = load_input(__file__).splitlines()

    total = 0
    for line in text_lines:
        matches = solve_line(line)
        if matches:
            total += rewards[matches - 1]
    return total


def solve2():
    text_lines = load_input(__file__).splitlines()

    solved = [
        {"i": i + 1, "count": 1, "score": solve_line(line)}
        for i, line in enumerate(text_lines)
    ]
    total = 0
    max_length = len(solved)
    for card in solved:
        i, count, score = card.values()
        total += count  # Total the cards in this stack

        range_end = i + score
        if range_end > max_length:
            range_end = max_length

        for target in solved[i:range_end]:
            target["count"] += count
    return total


def main():
    result_part_1 = solve1()
    result_part_2 = solve2()
    print(f"{result_part_1=}, {result_part_2=}")


if __name__ == "__main__":
    main()

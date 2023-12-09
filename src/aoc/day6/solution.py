import functools
import math
import operator

# Time:        44     80     65     72
# Distance:   208   1581   1050   1102

RACE_DATA = [(44, 208), (80, 1581), (65, 1050), (72, 1102)]


def iterative_solution(race_data: list[tuple]) -> int:
    record_beating_counts = []

    for total_time, record_distance in race_data:
        wins = []
        for button_time in range(1, total_time):
            velocity = button_time
            time_moving = total_time - button_time
            distance = time_moving * velocity
            if distance > record_distance:
                wins.append(distance)
        record_beating_counts.append(len(wins))

    result = functools.reduce(operator.mul, record_beating_counts)

    return result


def solve1():
    return iterative_solution(race_data=RACE_DATA)



def solve2():
    # Pretty sure this isn't a general solution but not sure why
    times, records = zip(*[(str(t), str(r)) for t, r in RACE_DATA])
    total_time, record_distance = int("".join(times)), int("".join(records))
    
    # Solve the quadratic inequality: (total_time - button_time) * button_time > record_distance
    # Rearranging gives: button_time^2 - total_time * button_time + record_distance < 0
    # Use quadratic formula to find the roots

    discriminant = total_time**2 - 4 * record_distance
    discriminant_root = math.sqrt(discriminant)

    root1 = (total_time - discriminant_root) / 2
    root2 = (total_time + discriminant_root) / 2

    # Count the number of integers between root1 and root2
    lower_bound = math.ceil(root1)
    upper_bound = math.floor(root2)

    result = max(0, upper_bound - lower_bound + 1)
    return result


def main():
    result_part_1 = solve1()
    result_part_2 = solve2()
    print(f"{result_part_1=}, {result_part_2=}")


if __name__ == "__main__":
    main()

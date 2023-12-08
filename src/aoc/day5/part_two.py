from aoc.day5.part_one import Maps
from aoc.utility import bump_range, load_input


class RangeMaps(Maps):
    def resolve_id_range(self, in_range: range) -> int:
        target = "seed"
        current_range = [in_range]

        while target and target != "location":
            key = self.find_key(target=target)
            maps = self.data[key]

            current_range = handle_ranges(current_range, maps)

            target = key[1]
        return current_range


def handle_ranges(source_ranges: range, maps: list[dict]) -> list[range]:
    """Sequentially fits all source ranges into the map ranges
     splitting the source range where it overlaps partially.
    Any source range that does fit into a map destination range is
     bumped by the offset (destination start - source start)
     converting it into the IDs of the destination.
    Any source range that does not fit into any destination range is
        left as is, those ids correlate 1:1.
    """
    queued = source_ranges
    complete = []
    while queued:
        current = queued.pop()
        # print(f"popped from queue: {current}. {queued=}")
        for m in maps:  # We need to look through every map
            map_range, offset = m.values()

            if current.start in map_range:
                if current.stop in map_range:
                    # Whole thing fits, bump by offset
                    # print(f"Complete fit")
                    complete.append(bump_range(current, offset))
                    current = None
                    break
                else:
                    # Partial fit, queue remainder, bump fit part by offset
                    overlap = range(current.start, map_range.stop)
                    remainder = range(map_range.stop, current.stop)
                    # print(f"Partial fit. Queueing {remainder}, completed: {overlap}")
                    queued.append(remainder)
                    complete.append(bump_range(overlap, offset))
                    current = None
                    break
            elif map_range.start in current:
                # Some sub-set fits in a map range
                before = range(current.start, map_range.start)
                overlap = range(map_range.start, map_range.stop)
                after = range(map_range.stop, current.stop)
                # print(f"Range fit withing source. Queueing {before, after}, completed: {overlap}")
                queued.extend([before, after])
                complete.append(bump_range(overlap, offset))
                current = None
                break
        # If current made it through all maps, it becomes complete
        if current:
            # print(f"Did not fit any map, completed: {current}")
            complete.append(current)

    return complete


def solve2():
    raw_lines = load_input(__file__).splitlines()
    seed_line = [int(seed) for seed in raw_lines.pop(0).split(":")[1].split()]
    seed_pairs = zip(seed_line[::2], seed_line[1::2])
    seed_ranges = [range(start, start + length) for start, length in seed_pairs]

    m = RangeMaps.from_lines(raw_lines)
    result_ranges = []
    _ = [
        result_ranges.extend(m.resolve_id_range(seed_range))
        for seed_range in seed_ranges
    ]
    result = min([r.start for r in result_ranges])
    return result

import string
from collections import defaultdict
from functools import total_ordering

from aocd import get_data


data = get_data(day=5, year=2023)
example = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

used_data = data


@total_ordering
class Interval:
    def __init__(self, start, end):
        self._start = start
        self._end = end

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    def __sub__(self, other):
        return Interval(self.start - other.start, self.end - other.end)

    def __add__(self, other):
        return Interval(self.start + other.start, self.end + other.end)

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash((self._start, self._end))

    def __contains__(self, item):
        return self.start <= item.start and item.end <= self.end

    def __lt__(self, other):
        return self.start < other.start

    def __repr__(self):
        return f"[{self.start}, {self.end}]"


def intersect(reference, tested):
    if (
        tested in reference
        or (tested < reference and tested.end < reference.start)
        or (tested > reference and tested.start > reference.end)
    ):
        return []
    if reference in tested:
        if reference.start == tested.start:
            return [
                reference,
                Interval(reference.end + 1, tested.end),
            ]
        if reference.end == tested.end:
            return [
                Interval(tested.start, reference.start - 1),
                reference,
            ]
        return [
            Interval(tested.start, reference.start - 1),
            reference,
            Interval(reference.end + 1, tested.end),
        ]
    if tested < reference:
        return [
            Interval(tested.start, reference.start - 1),
            Interval(reference.start, tested.end),
        ]
    return [
        Interval(tested.start, reference.end),
        Interval(reference.end + 1, tested.end),
    ]


def parse_seeds(seed_line):
    seeds_int = [int(seed) for seed in seed_line.split(": ")[1].split(" ")]
    seeds = []
    for i in range(0, len(seeds_int), 2):
        start, length = seeds_int[i : i + 2]
        seeds.append(Interval(start, start + length - 1))
    return seeds


def parse_mappings(blocks):
    mappings = []
    for block in blocks:
        lines = block.split("\n")
        mapping = {}
        for line in lines[1:]:
            dest_start, source_start, length = [int(s) for s in line.split(" ")]
            mapping[Interval(source_start, source_start + length - 1)] = Interval(
                dest_start, dest_start + length - 1
            )
        mappings.append(mapping)
    return mappings


blocks = used_data.split("\n\n")
seeds = parse_seeds(blocks[0])
mappings = parse_mappings(blocks[1:])
queue = seeds
for mapping in mappings:
    after = []
    while queue:
        print(queue)
        interval = queue.pop(0)
        for reference, target in mapping.items():
            if interval in reference:
                after.append(interval - reference + target)
                break
            if intersection := intersect(reference, interval):
                print(f"{reference=}, {interval=}, {intersection=}")
                queue.extend(intersection)
                break
        else:
            after.append(interval)
    queue = after


print(sorted(queue)[0].start)

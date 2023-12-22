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
used_input = data


class CategoryMap:
    def __init__(self, ranges):
        self.ranges = [[int(number) for number in line.split(" ")] for line in ranges]

    def get(self, number, default):
        for destination_start, source_start, length in self.ranges:
            if 0 <= (diff := number-source_start) < length:
                return destination_start + diff
        return default


def build_map(block):
    return CategoryMap(block.split("\n")[1:])


blocks = used_input.split("\n\n")
seeds = [int(seed) for seed in blocks[0].split(": ")[1].split(" ")]
maps = [build_map(block) for block in blocks[1:]]

running_min = None
for seed in seeds:
    current = seed
    for map in maps:
        current = map.get(current, current)
    if running_min is None or current < running_min:
        running_min = current

print(running_min)

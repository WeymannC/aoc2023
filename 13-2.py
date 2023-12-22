from functools import cache
from itertools import cycle, combinations
from math import lcm

from aocd import get_data

data = get_data(day=13, year=2023)
example = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
used_input = data

blocks = used_input.split("\n\n")


def find_mirror_plane(image):
    for i in range(1, len(image)):
        before, after = image[:i], image[i:]
        found = False
        for b, a in zip(before[::-1], after):
            if a != b:
                for element_a, element_b in zip(a, b):
                    if element_a != element_b:
                        if not found:
                            found = True
                        else:
                            break
                else:
                    continue
                break
        else:
            if found:
                return i
    return 0


total = 0
for block in blocks:
    lines = block.split("\n")
    total += 100 * find_mirror_plane(lines)
    columns = [[line[i] for line in lines] for i in range(len(lines[0]))]
    total += find_mirror_plane(columns)
print(total)

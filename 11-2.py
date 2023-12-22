from itertools import cycle, combinations
from math import lcm

from aocd import get_data

data = get_data(day=11, year=2023)
example = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
used_input = data

expansion_factor = 1_000_000

grid = [[c for c in line] for line in used_input.split("\n")]

lines_to_expand = [i for i, line in enumerate(grid) if all(c == "." for c in line)]
collumns_to_expand = [i for i in range(len(grid[0])) if all(line[i] =="." for line in grid)]
print(lines_to_expand, collumns_to_expand)

positions = {}
counter = 0
for j, line in enumerate(grid):
    for i, char in enumerate(line):
        if char == "#":
            positions[counter] = (i,j)
            counter += 1
print(positions)

total = 0
for (i, j), (k, l) in combinations(positions.values(), 2):
    horizontal_distance = abs(i-k)
    for index in collumns_to_expand:
        if (i < index < k) or (k < index < i):
            horizontal_distance += expansion_factor-1
    vertical_distance = abs(j-l)
    for index in lines_to_expand:
        if (j < index < l) or (l < index < j):
            vertical_distance += expansion_factor-1

    total += horizontal_distance + vertical_distance

print("\n".join("".join(line) for line in grid))
print(total)

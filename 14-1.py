from functools import cache
from itertools import cycle, combinations
from math import lcm

from aocd import get_data

data = get_data(day=14, year=2023)
example = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
used_input = data

grid = [[c for c in line] for line in used_input.split("\n")]

for j, line in enumerate(grid):
    for i, c in enumerate(line):
        if c == "O":
            count = 0
            start = 0
            for l, above in enumerate([line[i] for line in grid[:j]]):
                if above == "#":
                    count = 0
                    start = l + 1
                elif above == "O":
                    count += 1
            grid[j][i] = "."
            grid[start + count][i] = "O"

print("\n".join("".join(line) for line in grid))

total = 0
for j, line in enumerate(grid[::-1]):
    for c in line:
        if c == "O":
            total += j + 1
print(total)

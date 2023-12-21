import string
from collections import defaultdict
from functools import total_ordering
from itertools import pairwise

from aocd import get_data

data = get_data(day=16, year=2023)
example = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""
used_input = data

grid = [[c for c in line] for line in used_input.split("\n")]
x_dim = len(grid[0])
y_dim = len(grid)
assert all(len(line) == x_dim for line in grid)

deltas = {
    (">", "."): [((1, 0), ">")],
    ("<", "."): [((-1, 0), "<")],
    ("v", "."): [((0, 1), "v")],
    ("^", "."): [((0, -1), "^")],
    (">", "/"): [((0, -1), "^")],
    ("<", "/"): [((0, 1), "v")],
    ("v", "/"): [((-1, 0), "<")],
    ("^", "/"): [((1, 0), ">")],
    (">", "\\"): [((0, 1), "v")],
    ("<", "\\"): [((0, -1), "^")],
    ("v", "\\"): [((1, 0), ">")],
    ("^", "\\"): [((-1, 0), "<")],
    (">", "|"): [((0, 1), "v"), ((0, -1), "^")],
    ("<", "|"): [((0, 1), "v"), ((0, -1), "^")],
    ("v", "|"): [((0, 1), "v")],
    ("^", "|"): [((0, -1), "^")],
    (">", "-"): [((1, 0), ">")],
    ("<", "-"): [((-1, 0), "<")],
    ("v", "-"): [((1, 0), ">"), ((-1, 0), "<")],
    ("^", "-"): [((1, 0), ">"), ((-1, 0), "<")],
}


def next_positions(position, direction):
    i, j = position
    tile = grid[j][i]
    return [((i + di, j + dj), d) for (di, dj), d in deltas[(direction, tile)] if
            0 <= i + di < x_dim and 0 <= j + dj < y_dim]


starting_options = (
        [((0, j), ">") for j in range(y_dim)]
        + [((x_dim - 1, j), "<") for j in range(y_dim)]
        + [((i, 0), "v") for i in range(x_dim)]
        + [((i, y_dim - 1), "^") for i in range(x_dim)]
)
max_energy = 0
for starting_option in starting_options:
    positions = [starting_option]
    energized = {starting_option[0]}
    for position, direction in positions:
        positions.extend(pd for pd in next_positions(position, direction) if pd not in positions)
        energized.add(position)
    max_energy = max(max_energy, len(energized))
    print(starting_option, len(energized))
print(max_energy)

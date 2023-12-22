from collections import defaultdict
from contextlib import suppress
from functools import cache
from itertools import cycle, combinations
from math import lcm

from aocd import get_data

data = get_data(day=18, year=2023)
example = r"""R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""
used_input = data

lines = used_input.split("\n")

direction_strs = ["R", "D", "L", "U"]
directions = {
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (1, 0),
}
correction = {
    ("R", "D"): (1, 0),
    ("U", "R"): (0, 0),
    ("L", "U"): (0, -1),
    ("D", "L"): (1, -1),
    ("L", "D"): (1, -1),
    ("D", "R"): (1, 0),
    ("R", "U"): (0, 0),
    ("U", "L"): (0, -1),
}

current_position = (0, 0)
vertices = [current_position]
previous_direction = "U"
for line in lines:
    hex_code = line.split(" ")[-1].strip("()#")
    length = int(hex_code[:-1], base=16)
    direction = direction_strs[int(hex_code[-1])]

    x, y = vertices.pop()
    dx, dy = correction[(previous_direction, direction)]
    vertices.append((x + dx, y + dy))
    previous_direction = direction

    dx, dy = directions[direction]
    x, y = current_position
    current_position = (x + length * dx, y + length * dy)
    vertices.append(current_position)

total = 0
for (x1, y1), (x2, y2) in zip(vertices[:-1], vertices[1:]):
    total += x1 * y2 - x2 * y1
total /= 2
total = abs(total)

print(vertices)
print(total)

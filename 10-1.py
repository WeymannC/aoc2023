import string
from collections import defaultdict
from functools import total_ordering
from itertools import pairwise

from aocd import get_data


data = get_data(day=10, year=2023)
example = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""
used_data = data

grid = [[c for c in line] for line in used_data.split("\n")]
connected = {
    "|": ["N", "S"],
    "-": ["E", "W"],
    "L": ["N", "E"],
    "J": ["N", "W"],
    "7": ["S", "W"],
    "F": ["S", "E"],
    ".": [],
}


def connected_points(point):
    i, j = point
    if i < 0 or i >= len(grid[0]) or j < 0 or j >= len(grid):
        return []
    symbol = grid[j][i]
    if symbol == "S":
        return [
            neighbor
            for neighbor in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
            if point in connected_points(neighbor)
        ]
    directions = connected[symbol]
    points = []
    for direction in directions:
        if direction == "N":
            points.append((i, j - 1))
            continue
        if direction == "S":
            points.append((i, j + 1))
            continue
        if direction == "E":
            points.append((i + 1, j))
            continue
        if direction == "W":
            points.append((i - 1, j))
            continue
    return points


for j, line in enumerate(grid):
    for i, c in enumerate(line):
        if c == "S":
            starting_position = (i, j)
            break
    else:
        continue
    break

length = 0
points = [starting_position]
visited_points = []
while True:
    new_points = []
    visited_points.extend(points)
    for point in points:
        new_points.extend(
            [
                p
                for p in connected_points(point)
                if p not in visited_points and p not in new_points
            ]
        )
    length += 1
    if len(new_points) == 1:
        break
    points = new_points

print(length)

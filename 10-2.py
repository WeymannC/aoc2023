import string
from collections import defaultdict
from functools import total_ordering
from itertools import pairwise

from aocd import get_data


data = get_data(day=10, year=2023)
example = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""
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
            [
                neighbor
                for neighbor in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
                if point in connected_points(neighbor)
            ][0]
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
loop = []
while True:
    new_points = []
    loop.extend(points)
    for point in points:
        new_points.extend(
            [
                p
                for p in connected_points(point)
                if p not in loop and p not in new_points
            ]
        )
    length += 1
    if not new_points:
        break
    points = new_points

print(length)


def write_if_not_loop(point, symbol):
    if point in loop:
        return
    i, j = point
    if i < 0 or i >= len(grid[0]) or j < 0 or j >= len(grid):
        return
    grid[j][i] = symbol


loop.append(starting_position)
for (i, j), (k, l) in pairwise(loop):
    symbol = grid[l][k]
    dx = k - i
    dy = l - j
    if symbol == "|":
        if dy == 1:
            inside = [(k - 1, l)]
            outside = [(k + 1, l)]
        else:
            inside = [(k + 1, l)]
            outside = [(k - 1, l)]
    elif symbol == "-":
        if dx == 1:
            inside = [(k, l + 1)]
            outside = [(k, l - 1)]
        else:
            inside = [(k, l - 1)]
            outside = [(k, l + 1)]
    elif symbol == "L":
        if dy == 1:
            inside = [(k - 1, l), (k, l + 1)]
            outside = []
        else:
            inside = []
            outside = [(k - 1, l), (k, l + 1)]
    elif symbol == "J":
        if dy == 1:
            inside = []
            outside = [(k + 1, l), (k, l + 1)]
        else:
            inside = [(k + 1, l), (k, l + 1)]
            outside = []
    elif symbol == "7":
        if dy == -1:
            inside = [(k + 1, l), (k, l - 1)]
            outside = []
        else:
            inside = []
            outside = [(k + 1, l), (k, l - 1)]
    elif symbol == "F":
        if dy == -1:
            inside = []
            outside = [(k - 1, l), (k, l - 1)]
        else:
            inside = [(k - 1, l), (k, l - 1)]
            outside = []

    for p in inside:
        write_if_not_loop(p, "I")
    for p in outside:
        write_if_not_loop(p, "O")


def get_from_grid(point):
    i, j = point
    if i < 0 or i >= len(grid[0]) or j < 0 or j >= len(grid):
        return
    return grid[j][i]


for j, line in enumerate(grid):
    for i, symbol in enumerate(line):
        if (i, j) in loop:
            continue
        if symbol == "I" or symbol == "O":
            points = [(i, j)]
            visited_points = set()
            while points:
                print(points)
                point = points.pop(0)
                if point in visited_points:
                    continue
                visited_points.add(point)
                k, l = point
                if k < 0 or k >= len(grid[0]) or l < 0 or l >= len(grid):
                    continue
                write_if_not_loop(point, symbol)
                points.extend(
                    p
                    for p in [(k + 1, l), (k - 1, l), (k, l + 1), (k, l - 1)]
                    if p not in visited_points
                    and p not in loop
                    and get_from_grid(p) not in [None, "I", "O"]
                )


print("\n".join([" ".join(line) for line in grid]))
print(sum(1 for line in grid for c in line if c == "I"))
print(sum(1 for line in grid for c in line if c == "O"))

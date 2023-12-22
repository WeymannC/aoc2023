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
spin_cycles = 1_000_000_000

lines = used_input.split("\n")


def move(line):
    """Move all 'O's to the right of their group"""
    return "#".join("".join(sorted(group)) for group in line.split("#"))


def move_north(lines):
    north_lines = [
        "".join(line[i] for line in lines[::-1]) for i in range(len(lines[0]))
    ]
    north_lines = [move(line) for line in north_lines]
    return [
        "".join(line[i] for line in north_lines)
        for i in reversed(range(len(north_lines)))
    ]


def move_west(lines):
    west_lines = ["".join(reversed(line)) for line in lines]
    west_lines = [move(line) for line in west_lines]
    return ["".join(reversed(line)) for line in west_lines]


def move_south(lines):
    south_lines = ["".join(line[i] for line in lines) for i in range(len(lines[0]))]
    south_lines = [move(line) for line in south_lines]
    return ["".join(line[i] for line in south_lines) for i in range(len(south_lines))]


def move_east(lines):
    return [move(line) for line in lines]


def spin_cycle(lines):
    lines = move_north(lines)
    lines = move_west(lines)
    lines = move_south(lines)
    lines = move_east(lines)
    return lines


known_positions = [lines]
for i in range(spin_cycles):
    lines = spin_cycle(lines)
    if lines in known_positions:
        start = known_positions.index(lines)
        print(start)
        length = i + 1 - start
        print(length)
        remaining_cycles = (spin_cycles - start) % length
        print(remaining_cycles)
        lines = known_positions[start + remaining_cycles]
        break
    known_positions.append(lines)

total = 0
for j, line in enumerate(lines[::-1]):
    for c in line:
        if c == "O":
            total += j + 1
print(total)

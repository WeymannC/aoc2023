import json
from collections import namedtuple, defaultdict
from functools import lru_cache
from pprint import pprint

from aocd import get_data

data = get_data(day=23, year=2023)
example = r"""#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""
used_input = data

lines = used_input.split("\n")
x_dim = len(lines[0])
y_dim = len(lines)


slopes = {
    "<": (-1, 0),
    ">": (1, 0),
    "v": (0, 1),
    "^": (0, -1),
}


def next_steps(i, j):
    if (point := lines[j][i]) == ".":
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    else:
        directions = [slopes[point]]
    return [
        (i + di, j + dj)
        for di, dj in directions
        if 0 <= i + di < x_dim and 0 <= j + dj < y_dim and lines[j + dj][i + di] != "#"
    ]


def is_node(i, j):
    return (
        len(
            [
                lines[j + dj][i + di]
                for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]
                if 0 <= i + di < x_dim
                and 0 <= j + dj < y_dim
                and lines[j + dj][i + di] != "#"
            ]
        )
        > 2
    )


nodes = defaultdict(list)
starting_point = (lines[0].index("."), 0)
target = (lines[-1].index("."), y_dim - 1)

length = 0
steps = [(starting_point, starting_point, None, 0)]
while steps:
    current_node, current_step, previous_step, length = steps.pop()
    if current_step == target:
        nodes[current_node].append((target, length))
        continue
    if is_node(*current_step):
        nodes[current_node].append((current_step, length))
        length = 0
        current_node = current_step
        if current_step in nodes:
            continue
    length += 1
    steps.extend(
        (current_node, step, current_step, length)
        for step in next_steps(*current_step)
        if step != previous_step
    )

pprint(nodes)


@lru_cache
def longest_path_to_target(node):
    if node == target:
        return 0
    return max(length + longest_path_to_target(n) for n, length in nodes[node])


print(longest_path_to_target(starting_point))

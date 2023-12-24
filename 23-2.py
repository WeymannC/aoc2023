import json
from collections import namedtuple, defaultdict
from functools import lru_cache
from math import inf
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


def next_steps(i, j):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
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


nodes = defaultdict(set)
starting_point = (lines[0].index("."), 0)
target = (lines[-1].index("."), y_dim - 1)

length = 0
steps = [(starting_point, starting_point, None, 0)]
while steps:
    current_node, current_step, previous_step, length = steps.pop()
    if current_step == target:
        nodes[current_node].add((target, length))
        nodes[target].add((current_node, length))
        continue
    if is_node(*current_step):
        visited = current_step in nodes
        nodes[current_node].add((current_step, length))
        nodes[current_step].add((current_node, length))
        length = 0
        current_node = current_step
        if visited:
            continue
    length += 1
    steps.extend(
        (current_node, step, current_step, length)
        for step in next_steps(*current_step)
        if step != previous_step
    )

pprint(nodes)


@lru_cache
def longest_path_to_target(node, visited):
    if node == target:
        return 0
    if all(n in visited for n, _ in nodes[node]):
        return -inf
    v = visited | {node}
    result = max(
        length + longest_path_to_target(n, v)
        for n, length in nodes[node]
        if n not in visited
    )
    print(node, result)
    return result


print(longest_path_to_target(starting_point, frozenset()))

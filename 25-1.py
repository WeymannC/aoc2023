import json
import random
from collections import namedtuple, defaultdict
from functools import lru_cache
from math import inf
from pprint import pprint

from aocd import get_data

data = get_data(day=25, year=2023)
example = r"""jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""
used_input = data

lines = used_input.split("\n")


def init_vertices(lines):
    vertices = defaultdict(list)
    for line in lines:
        name, neighbour_str = line.split(": ")
        vertices[name].extend(neighbour_str.split(" "))
        for neighbour in vertices[name]:
            if name not in vertices[neighbour]:
                vertices[neighbour].append(name)
    return vertices


def merge(v1, v2, vertices):
    combined = f"{v1}, {v2}"
    vertices[combined] = [v for v in (vertices[v1] + vertices[v2]) if v not in [v1, v2]]
    for v in vertices[combined]:
        vertices[v] = [combined if vv in [v1, v2] else vv for vv in vertices[v]]
    del vertices[v1]
    del vertices[v2]


def get_random_edge(vertices):
    v1 = random.choices(
        list(vertices.keys()), [len(neighbours) for neighbours in vertices.values()]
    )[0]
    v2 = random.choice(vertices[v1])
    return v1, v2


def reduce(vertices):
    while len(vertices) > 2:
        merge(*get_random_edge(vertices), vertices)


while True:
    vertices = init_vertices(lines)
    reduce(vertices)
    if all(len(ns) == 3 for ns in vertices.values()):
        break

result = 1
for key in vertices:
    print(key)
    result *= len(key.split(", "))
print(result)

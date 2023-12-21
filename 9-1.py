import string
from collections import defaultdict
from functools import total_ordering
from itertools import pairwise

from aocd import get_data


data = get_data(day=9, year=2023)
example = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
used_data = data


def project(history):
    last_elements = []
    while not all(point == 0 for point in history):
        last_elements.append(history[-1])
        history = [y - x for x, y in pairwise(history)]
    return sum(last_elements)


histories = [[int(s) for s in line.split(" ")] for line in used_data.split("\n")]
total = 0
for history in histories:
    total += project(history)
print(total)

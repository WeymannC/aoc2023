from functools import cache
from itertools import cycle, combinations
from math import lcm

from aocd import get_data

data = get_data(day=15, year=2023)
example = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""
used_input = data


def build_hash(group):
    current = 0
    for c in group:
        current += ord(c)
        current *= 17
        current %= 256
    return current


sequence = used_input.split(",")
total = 0
for group in sequence:
    total += build_hash(group)

print(total)

from collections import defaultdict
from contextlib import suppress
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
boxes = defaultdict(list)
focals = {}
for group in sequence:
    label = group.split("=")[0].split("-")[0]
    box = build_hash(label)
    if "-" in group:
        with suppress(ValueError):
            boxes[box].remove(label)
    elif "=" in group:
        focal = int(group.split("=")[1])
        focals[label] = focal
        if label not in boxes[box]:
            boxes[box].append(label)

total = 0
for box_no, box in boxes.items():
    for i, lens in enumerate(box):
        total += (i + 1) * (box_no + 1) * focals[lens]

print(total)

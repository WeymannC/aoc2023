import json
from collections import namedtuple, defaultdict
from functools import lru_cache
from math import inf
from pprint import pprint

from aocd import get_data

data = get_data(day=24, year=2023)
example = r"""19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
used_input = data
lower_bound = 200000000000000
upper_bound = 400000000000000

lines = used_input.split("\n")

points = []
for line in lines:
    position, speed = line.split(" @ ")
    x, y, z = [int(n) for n in position.split(", ")]
    dx, dy, dz = [int(n) for n in speed.split(", ")]
    points.append((x, y, z, dx, dy, dz))


def line_parameters(point):
    x, y, _, dx, dy, _ = point
    return dy / dx, y - dy / dx * x


def meet_in_future(point1, point2):
    x1, _, _, dx1, _, _ = point1
    x2, _, _, dx2, _, _ = point2
    a, b = line_parameters(point1)
    c, d = line_parameters(point2)
    if a == c:
        return False
    x_meet = (d - b) / (a - c)
    y_meet = a * x_meet + b
    return (
        lower_bound <= x_meet <= upper_bound
        and lower_bound <= y_meet <= upper_bound
        and ((dx1 > 0 and x_meet > x1) or (dx1 < 0 and x_meet < x1))
        and ((dx2 > 0 and x_meet > x2) or (dx2 < 0 and x_meet < x2))
    )


print(
    sum(
        1
        for i, point1 in enumerate(points)
        for point2 in points[i + 1 :]
        if meet_in_future(point1, point2)
    )
)

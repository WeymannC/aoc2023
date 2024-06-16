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


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Vector(other * self.x, other * self.y, other * self.z)

    def cross(self, other):
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z


lines = used_input.split("\n")

points = []
for line in lines:
    position, speed = line.split(" @ ")
    x, y, z = [int(n) for n in position.split(", ")]
    dx, dy, dz = [int(n) for n in speed.split(", ")]
    points.append((Vector(x, y, z), Vector(dx, dy, dz)))

pos_0, vel_0 = points[0]
pos_1, vel_1 = points[1]
pos_2, vel_2 = points[2]

p_1 = pos_1 - pos_0
v_1 = vel_1 - vel_0
p_2 = pos_2 - pos_0
v_2 = vel_2 - vel_0

t_1 = -(p_1.cross(p_2).dot(v_2) / v_1.cross(p_2).dot(v_2))
t_2 = -(p_1.cross(p_2).dot(v_1) / p_1.cross(v_2).dot(v_1))

c_1 = pos_1 + vel_1 * t_1
c_2 = pos_2 + vel_2 * t_2
v = (c_2 - c_1) * (1 / (t_2 - t_1))
p = c_1 - v * t_1

print(p.x + p.y + p.z)

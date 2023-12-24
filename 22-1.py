import json
from collections import namedtuple, defaultdict
from functools import lru_cache
from pprint import pprint

from aocd import get_data

data = get_data(day=22, year=2023)
example = r"""1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""
used_input = data

lines = used_input.split("\n")

grid = defaultdict(lambda: (0, None))

Brick = namedtuple("Brick", ["x", "y", "z", "supported_by", "supports"])

bricks = []
for line in lines:
    (xmin, ymin, zmin), (xmax, ymax, zmax) = [eval(t) for t in line.split("~")]
    bricks.append(Brick(range(xmin, xmax + 1), range(ymin, ymax + 1), range(zmin, zmax + 1), set(), set()))
bricks.sort(key=lambda b: b.z[0])

for i, brick in enumerate(bricks):
    current_height, _ = max((grid[(x, y)] for x in brick.x for y in brick.y), key=lambda p: p[0])
    next_height = current_height + len(brick.z)
    for x in brick.x:
        for y in brick.y:
            height, current_brick = grid[(x,y)]
            if height == current_height:
                if current_brick is not None:
                    current_index = bricks.index(current_brick)
                    brick.supported_by.add(current_index)
                    current_brick.supports.add(i)
            grid[(x, y)] = (next_height, brick)

for i, brick in enumerate(bricks):
    print(i, brick)

destroyable = [
    brick for brick in bricks
    if all(len(bricks[i].supported_by) > 1 for i in brick.supports)]
pprint(destroyable)
print(len(destroyable))

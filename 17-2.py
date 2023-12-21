import string
from collections import defaultdict, namedtuple
from functools import total_ordering
from itertools import pairwise

from aocd import get_data

data = get_data(day=17, year=2023)
example = r"""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
example2= r"""111111111111
999999999991
999999999991
999999999991
999999999991"""
used_input = data

grid = [[int(c) for c in line] for line in used_input.split("\n")]
x_dim = len(grid[0])
y_dim = len(grid)
print(x_dim, y_dim)

Position = namedtuple("Position", ["x", "y"])
Step = namedtuple("Step", ["position", "direction", "streak"])

deltas = {
    "<": (-1, 0),
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
}

reverse = {
    ">": "<",
    "<": ">",
    "v": "^",
    "^": "v",
}


def next_steps(step):
    i, j = step.position
    options=[]
    for direction, delta in deltas.items():
        if direction == reverse[step.direction]:
            continue
        if direction != step.direction and step.streak < 4:
            continue
        di, dj = delta
        if not (0 <= i + di < x_dim and 0 <= j + dj < y_dim):
            continue
        next_position = Position(i + di, j + dj)
        if direction == step.direction:
            if step.streak >= 10:
                continue
            options.append(Step(next_position, direction, step.streak +1))
        else:
            options.append(Step(next_position, direction, 1))

    return options


starting_step = Step(Position(0,0), ">", 0)
goal = Position(x_dim-1, y_dim-1)
known_steps = {starting_step: 0}
steps = [(step, 0) for step in next_steps(starting_step)]
current_min = 10 * (x_dim + y_dim)
while steps:
    step, prev_loss = steps.pop()
    i, j = step.position
    loss = prev_loss + grid[j][i]
    if loss >= current_min:
        continue
    if step.position == goal and step.streak >= 4:
        current_min = min(current_min, loss)
        print(current_min)
        continue
    if step in known_steps and known_steps[step] <= loss:
        continue
    known_steps[step] = loss
    steps.extend([(s, loss) for s in next_steps(step)])

print(current_min)


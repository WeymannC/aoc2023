from itertools import cycle
from math import lcm

from aocd import get_data

data = get_data(day=8, year=2023)
example = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
used_input = data


class Ghost:
    def __init__(self, initial_node):
        self.found_cycle = False
        self.steps = [(0, initial_node)]
        self.goals = []
        self.length_cycle = None
        self.offset = None

    def add_step(self, i, key):
        if self.found_cycle:
            return
        if (i, key) in self.steps:
            self.found_cycle = True
            self.offset = self.steps.index((i, key)) - 1
            self.length_cycle = len(self.steps) - self.offset -1
            #self.goals = [(g - self.offset) % self.length_cycle + self.offset for g in self.goals]

        else:
            self.steps.append((i, key))
            if key.endswith("Z"):
                self.goals.append(len(self.steps))

    @property
    def current_node(self):
        return nodes[self.steps[-1][1]]

    def __repr__(self):
        return f"{self.steps}, {self.goals}, {self.length_cycle}, {self.offset}"


instructions = used_input.split("\n\n")[0]
nodes = {}
for line in used_input.split("\n\n")[1].split("\n"):
    key, value_str = line.split(" = ")
    value = value_str.strip("()").split(", ")
    nodes[key] = value

total = 0
ghosts = [Ghost(node_key) for node_key in nodes if node_key.endswith("A")]
for i, direction in cycle(enumerate(instructions)):
    for ghost in ghosts:
        if ghost.found_cycle:
            continue
        if direction == "L":
            ghost.add_step(i + 1, ghost.current_node[0])
        elif direction== "R":
            ghost.add_step(i + 1, ghost.current_node[1])
        else:
            raise ValueError(f"Received direction {direction}")
    total += 1
    if all(ghost.found_cycle for ghost in ghosts):
        break
print(total)
print(lcm(*[ghost.goals[0] -1  for ghost in ghosts]))

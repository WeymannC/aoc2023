from itertools import cycle

from aocd import get_data

data = get_data(day=8, year=2023)
example = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""
example2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
used_input = data

instructions = used_input.split("\n\n")[0]
nodes = {}
for line in used_input.split("\n\n")[1].split("\n"):
    key, value_str = line.split(" = ")
    value = value_str.strip("()").split(", ")
    nodes[key] = value

total = 0
current_node = nodes["AAA"]
for direction in cycle(instructions):
    if direction == "L":
        next_node_key = current_node[0]
    elif direction== "R":
        next_node_key = current_node[1]
    else:
        raise ValueError(f"Received direction {direction}")
    total += 1
    if next_node_key == "ZZZ":
        break
    current_node = nodes[next_node_key]

print(total)

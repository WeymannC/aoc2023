from itertools import cycle, combinations
from math import lcm

from aocd import get_data

data = get_data(day=12, year=2023)
example = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
used_input = data


def parse_groups(constraint):
    counter = 0
    groups = []
    for c in constraint:
        if c == "#":
            counter += 1
        elif c == ".":
            if counter > 0:
                groups.append(counter)
                counter = 0
    if counter > 0:
        groups.append(counter)
    return groups


def build_options(hints, length, constraint):
    if "?" not in constraint:
        if parse_groups(constraint) == hints:
            return [constraint]
        else:
            return []
    if not hints:
        if all(c in [".", "?"] for c in constraint):
            return ["." * length]
        return []
    if sum(hints) + len(hints) - 1 > length:
        return []

    empty_start = "."
    if all(c in [o, "?"] for o, c in zip(empty_start, constraint)):
        empty_options = [
            empty_start + option
            for option in build_options(hints, length - 1, constraint[1:])
        ]
    else:
        empty_options = []
    spring_start = "#" * hints[0] + ("." if len(hints) > 1 else "")
    if all(c in [o, "?"] for o, c in zip(spring_start, constraint)):
        spring_options = [
            spring_start + option
            for option in build_options(
                hints[1:], length - len(spring_start), constraint[len(spring_start) :]
            )
        ]
    else:
        spring_options = []
    return empty_options + spring_options


lines = used_input.split("\n")

total = 0
for line in lines:
    print(line)
    constraint, hints_str = line.split(" ")
    hints = eval(f"[{hints_str}]")
    length = len(constraint)
    options = build_options(hints, length, constraint)
    print("\n".join(options))
    total += len(options)
print(total)

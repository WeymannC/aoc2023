from functools import cache
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


@cache
def count_options(hints, constraint):
    if not hints:
        if all(c in [".", "?"] for c in constraint):
            return 1
        return 0
    if sum(hints) + len(hints) - 1 > len(constraint):
        return 0

    if constraint[0] in [".", "?"]:
        empty_options = count_options(hints, constraint[1:])
    else:
        empty_options = 0
    spring_start = hints[0] + (1 if len(hints) > 1 else 0)
    if all(c in ["#", "?"] for c in constraint[: hints[0]]) and (
        len(constraint) == hints[0] or constraint[hints[0]] in [".", "?"]
    ):
        spring_options = count_options(hints[1:], constraint[spring_start:])

    else:
        spring_options = 0
    return empty_options + spring_options


lines = used_input.split("\n")

total = 0
for line in lines:
    print(line)
    folded_constraint, hints_str = line.split(" ")
    constraint = "?".join([folded_constraint] * 5)
    hints = eval(f"({hints_str})") * 5
    total += count_options(hints, constraint)
print(total)

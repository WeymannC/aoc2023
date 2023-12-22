from collections import defaultdict, namedtuple
from contextlib import suppress
from functools import cache
from itertools import cycle, combinations
from math import lcm

from aocd import get_data

data = get_data(day=19, year=2023)
example = r"""px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""
used_input = data

workflow_strs, part_strs = used_input.split("\n\n")

Part = namedtuple("Part", ["x", "m", "a", "s"])
parts = []
for part_str in part_strs.split("\n"):
    props = {}
    for s in part_str.strip("{}").split(","):
        key, value = s.split("=")
        props[key] = int(value)
    parts.append(Part(**props))


class Workflow:
    def __init__(self, workflow_str):
        self.name, rules = workflow_str.split("{")
        self.rules = rules.strip("}").split(",")
        self.default = self.rules.pop()

    def __call__(self, part):
        x, m, a, s = part
        for rule in self.rules:
            if eval(rule.split(":")[0]):
                return rule.split(":")[1]
        return self.default


workflows = {
    workflow.name: workflow
    for workflow in (
        Workflow(workflow_str) for workflow_str in workflow_strs.split("\n")
    )
}

total = 0
for part in parts:
    next_workflow = "in"
    while next_workflow != "R":
        next_workflow = workflows[next_workflow](part)
        if next_workflow == "A":
            total += sum(part)
            break

print(total)

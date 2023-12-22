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

workflow_strs, _ = used_input.split("\n\n")

Part = namedtuple("Part", ["x", "m", "a", "s"])


class PartRange(Part):
    def split(self, attr, condition, limit):
        min_attr, max_attr = self.__getattribute__(attr)
        if min_attr <= limit <= max_attr:
            if condition == "<":
                return self._replace(**{attr: (min_attr, limit - 1)}), self._replace(
                    **{attr: (limit, max_attr)}
                )
            return self._replace(**{attr: (limit + 1, max_attr)}), self._replace(
                **{attr: (min_attr, limit)}
            )
        elif limit < min_attr:
            if condition == "<":
                return None, self
            return self, None
        if condition == "<":
            return self, None
        return None, self

    def size(self):
        x0, x1 = self.x
        m0, m1 = self.m
        a0, a1 = self.a
        s0, s1 = self.s
        return (x1 - x0 + 1) * (m1 - m0 + 1) * (a1 - a0 + 1) * (s1 - s0 + 1)

    def overlap(self, other):
        args = []
        for (s0, s1), (o0, o1) in zip(self, other):
            r0 = max(s0, o0)
            r1 = min(s1, o1)
            if r0 > r1:
                return None
            args.append((r0, r1))
        return PartRange(*args)

    def __contains__(self, item):
        return self.overlap(item) == item


class Workflow:
    def __init__(self, workflow_str):
        self.name, rules = workflow_str.split("{")
        self.rules = rules.strip("}").split(",")
        self.default = self.rules.pop()

    def __call__(self, part_range):
        dest_ranges = defaultdict(list)
        current_range = part_range
        for rule in self.rules:
            attr = rule[0]
            condition = rule[1]
            limit_str, dest = rule[2:].split(":")
            limit = int(limit_str)
            passing_range, current_range = current_range.split(attr, condition, limit)
            if passing_range is not None:
                dest_ranges[dest].append(passing_range)
            if current_range is None:
                break
        else:
            dest_ranges[self.default].append(current_range)
        return dest_ranges


workflows = {
    workflow.name: workflow
    for workflow in (
        Workflow(workflow_str) for workflow_str in workflow_strs.split("\n")
    )
}

starting_range = PartRange(x=(1, 4000), m=(1, 4000), a=(1, 4000), s=(1, 4000))
incoming_ranges = defaultdict(list)
incoming_ranges["in"] = [starting_range]
accepted = []
while list(incoming_ranges):
    key = next(iter(incoming_ranges))
    workflow = workflows[key]
    ranges = incoming_ranges.pop(key)
    for range in ranges:
        destination_workflows = workflow(range)
        for k, v in destination_workflows.items():
            if k == "R":
                continue
            if k == "A":
                accepted.extend(v)
                continue
            incoming_ranges[k].extend(v)

total = 0
for block in accepted:
    total += block.size()

print(total)

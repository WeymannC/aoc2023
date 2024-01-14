import json
from abc import ABC, abstractmethod
from collections import defaultdict, namedtuple
from contextlib import suppress
from functools import cache
from itertools import cycle, combinations, count
from math import lcm

from aocd import get_data

data = get_data(day=20, year=2023)
example = r"""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""
example2 = r"""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
used_input = data

pulse_queue = []
pulse_count = {"low": 0, "high": 0}


class Module(ABC):
    def __init__(self, name, targets):
        self.name = name
        self.targets = targets
        self.incoming = []
        self.outgoing = []
        self.first_low = None
        self.first_high = None

    @abstractmethod
    def _call(self, iteration, pulse, origin):
        ...

    def __call__(self, iteration, pulse, origin):
        self.incoming.append(pulse)
        self._call(iteration, pulse, origin)

    @abstractmethod
    def state(self):
        ...

    def _send(self, i, pulse):
        self.outgoing.append(pulse)
        if pulse == "low" and self.first_low is None:
            self.first_low = i
        if pulse == "high" and self.first_high is None:
            self.first_high = i
        pulse_count[pulse] += len(self.targets)
        pulse_queue.extend((target, (pulse, self.name)) for target in self.targets)

    def report(self):
        return f"Incoming: {self.incoming}\nOutgoing: {self.outgoing}"

    def reset(self):
        self.incoming = []
        self.outgoing = []


class FlipFlop(Module):
    def __init__(self, name, targets):
        super().__init__(name, targets)
        self.on = False

    def _call(self, i, pulse, _):
        if pulse == "high":
            return
        if self.on:
            self.on = False
            self._send(i, "low")
        else:
            self.on = True
            self._send(i, "high")

    def state(self):
        return self.on


class Conjunction(Module):
    def __init__(self, name, targets):
        super().__init__(name, targets)
        self._origins = {}

    def _call(self, i, pulse, origin):
        self._origins[origin] = pulse
        if all(p == "high" for p in self._origins.values()):
            self._send(i, "low")
        else:
            self._send(i, "high")

    def state(self):
        return self._origins

    def register_origin(self, origin):
        self._origins[origin] = "low"


def push_button(broadcaster_targets):
    pulse_count["low"] += len(broadcaster_targets) + 1
    pulse_queue.extend(
        (target, ("low", "broadcaster")) for target in broadcaster_targets
    )


def parse_input(used_input):
    modules = {}
    broadcaster_targets = []
    for line in used_input.split("\n"):
        module_str, targets_str = line.split(" -> ")
        targets = targets_str.split(", ")
        if module_str == "broadcaster":
            broadcaster_targets = targets
            continue
        module_type, module_name = module_str[0], module_str[1:]
        if module_type == "%":
            modules[module_name] = FlipFlop(module_name, targets)
        elif module_type == "&":
            modules[module_name] = Conjunction(module_name, targets)
    for module in modules.values():
        if type(module) is Conjunction:
            for other in modules.values():
                if module.name in other.targets:
                    module.register_origin(other.name)
    final_conjunction = next(iter(m for m in modules.values() if "rx" in m.targets))
    final_origins = final_conjunction._origins
    return modules, broadcaster_targets, final_origins


modules, broadcaster_targets, final_origins = parse_input(used_input)
starting_state = {k: v.state() for k, v in modules.items()}
for i in count(1):
    push_button(broadcaster_targets)
    while pulse_queue:
        target_name, args = pulse_queue.pop(0)
        if target_name == "rx" and args[0] == "low":
            break
        modules.get(target_name, lambda *args: None)(i, *args)
    if all(modules[m].first_high is not None for m in final_origins):
        break

print(lcm(*[modules[m].first_high for m in final_origins]))

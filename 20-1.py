from abc import ABC, abstractmethod
from collections import defaultdict, namedtuple
from contextlib import suppress
from functools import cache
from itertools import cycle, combinations
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

    @abstractmethod
    def __call__(self, pulse, origin):
        ...

    @abstractmethod
    def state(self):
        ...

    def _send(self, pulse):
        pulse_count[pulse] += len(self.targets)
        pulse_queue.extend((target, (pulse, self.name)) for target in self.targets)


class FlipFlop(Module):
    def __init__(self, name, targets):
        super().__init__(name, targets)
        self.on = False

    def __call__(self, pulse, _):
        if pulse == "high":
            return
        if self.on:
            self.on = False
            self._send("low")
        else:
            self.on = True
            self._send("high")

    def state(self):
        return self.on


class Conjunction(Module):
    def __init__(self, name, targets):
        super().__init__(name, targets)
        self._origins = {}

    def __call__(self, pulse, origin):
        self._origins[origin] = pulse
        if all(p == "high" for p in self._origins.values()):
            self._send("low")
        else:
            self._send("high")

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

    return modules, broadcaster_targets


modules, broadcaster_targets = parse_input(used_input)
starting_state = {k: v.state() for k, v in modules.items()}
loop_length = 1000
for i in range(1000):
    push_button(broadcaster_targets)
    while pulse_queue:
        target_name, args = pulse_queue.pop(0)
        modules.get(target_name, lambda *args: None)(*args)
    if {k: v.state() for k, v in modules.items()} == starting_state:
        loop_length = i + 1
        break

print(loop_length)
pulse_count["low"] *= 1000 // loop_length
pulse_count["high"] *= 1000 // loop_length
for _ in range(1000 % loop_length):
    push_button(broadcaster_targets)
    while pulse_queue:
        target_name, args = pulse_queue.pop(0)
        modules[target_name](*args)

print(pulse_count["low"] * pulse_count["high"])

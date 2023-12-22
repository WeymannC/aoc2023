import string
import re

from aocd import get_data

data = get_data(day=1, year=2023)
example = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

used_input = data
lines = used_input.split("\n")

mapping = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

regex = rf"(?=([1-9]|{'|'.join(mapping)}))"
print(regex)
sum = 0
for line in lines:
    print(line)
    matches = [match.group(1) for match in re.finditer(regex, line)]
    print(matches)
    first_int = mapping.get(matches[0]) or int(matches[0])
    print(first_int)
    last_int = mapping.get(matches[-1]) or int(matches[-1])
    print(last_int)
    solution_int = 10*first_int + last_int
    print(solution_int)

    sum += solution_int

print(sum)

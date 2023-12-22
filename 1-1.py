import string

from aocd import get_data

data = get_data(day=1, year=2023)
example = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

used_input = data
lines = used_input.split("\n")

sum = 0
for line in lines:
    solution_string = ""
    for char in line:
        if char in string.digits:
            solution_string += char
            break
    for char in line[::-1]:
        if char in string.digits:
            solution_string += char
            break
    sum += int(solution_string)

print(sum)

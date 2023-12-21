import string
from collections import defaultdict

from aocd import get_data


data = get_data(day=3, year=2023)
example = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

used_data = data
lines = used_data.split("\n")

grid = [[char for char in line] for line in lines]
dim_x = len(grid[0])
dim_y = len(grid)
gears = defaultdict(list)


def process_neighbors(i, j, start_j, number):
    left_edge = max(start_j - 1, 0)
    right_edge = min(j + 1, dim_x)
    if i > 0:
        for j in range(left_edge, right_edge):
            if grid[i - 1][j] == "*":
                gears[(i - 1, j)].append(number)
    if i < dim_y - 1:
        for j in range(left_edge, right_edge):
            if grid[i + 1][j] == "*":
                gears[(i + 1, j)].append(number)
    if start_j > 0:
        if grid[i][start_j - 1] == "*":
            gears[(i, start_j - 1)].append(number)
    if j < dim_x - 1:
        if grid[i][j] == "*":
            gears[(i, j)].append(number)


for i in range(dim_y):
    in_number = False
    number_str = ""
    start_j = 0
    for j in range(dim_x):
        char = grid[i][j]
        if char in string.digits:
            if not in_number:
                start_j = j
            in_number = True
            number_str += char
        else:
            if in_number:
                number = int(number_str)
                process_neighbors(i, j, start_j, number)
            in_number = False
            number_str = ""
    else:
        if in_number:
            number = int(number_str)
            process_neighbors(i, dim_x - 1, start_j, number)

total = 0
for parts in gears.values():
    if len(parts) == 2:
        total += parts[0] * parts[1]

print(total)

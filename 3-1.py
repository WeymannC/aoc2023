import string

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

total = 0
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
                left_edge = max(start_j - 1, 0)
                right_edge = min(j + 1, dim_x)
                is_part = (
                    (
                        any(
                            neighbour not in (string.digits + ".")
                            for neighbour in grid[i - 1][left_edge:right_edge]
                        )
                        if i > 0
                        else False
                    )
                    or (
                        any(
                            neighbour not in (string.digits + ".")
                            for neighbour in grid[i + 1][left_edge:right_edge]
                        )
                        if i < dim_y - 1
                        else False
                    )
                    or (
                        grid[i][start_j - 1] not in (string.digits + ".")
                        if start_j > 0
                        else False
                    )
                    or (
                        grid[i][j] not in (string.digits + ".")
                        if j < dim_x - 1
                        else False
                    )
                )
                if is_part:
                    total += number
            in_number = False
            number_str = ""
    else:
        if in_number:
            number = int(number_str)
            left_edge = max(start_j - 1, 0)
            right_edge = dim_x
            is_part = (
                (
                    any(
                        neighbour not in (string.digits + ".")
                        for neighbour in grid[i - 1][left_edge:right_edge]
                    )
                    if i > 0
                    else False
                )
                or (
                    any(
                        neighbour not in (string.digits + ".")
                        for neighbour in grid[i + 1][left_edge:right_edge]
                    )
                    if i < dim_y - 1
                    else False
                )
                or (
                    grid[i][start_j - 1] not in (string.digits + ".")
                    if start_j > 0
                    else False
                )
            )
            if is_part:
                total += number

print(total)

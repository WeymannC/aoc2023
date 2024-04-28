from functools import lru_cache

from aocd import get_data

data = get_data(day=21, year=2023)
example = r"""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
used_input = data
steps = 26501365

lines = used_input.split("\n")
x_dim = len(lines[0])
y_dim = len(lines)

size = x_dim
M = steps // x_dim
corner = M * (M + 1)
edge = (M + 1) ** 2
filler = M**2

print(size, M, size // 2, steps % size)


def move(position, displacement):
    x, y = position
    dx, dy = displacement
    new_x, new_y = x + dx, y + dy
    if (new_x, new_y) in known_positions:
        return
    if not (0 <= new_x < x_dim and 0 <= new_y < y_dim):
        return
    if lines[new_y][new_x] == "#":
        return
    return new_x, new_y


def step(position):
    next_positions = set()
    for displacement in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        if next_position := move(position, displacement):
            next_positions.add(next_position)
    return next_positions


starting_position = [
    (x, y) for y, line in enumerate(lines) for x, char in enumerate(line) if char == "S"
][0]
known_positions = {starting_position: 0}
queue = [(starting_position, 0)]
while queue:
    current_position, distance = queue.pop(0)
    next_positions = step(current_position)
    for position in next_positions:
        known_positions[position] = distance + 1
        queue.append((position, distance + 1))


total = 0
for distance in known_positions.values():
    if distance > size // 2:
        total += corner
    elif distance % 2 == 1:
        total += edge
    else:
        total += filler
print(total)

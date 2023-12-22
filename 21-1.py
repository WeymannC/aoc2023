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
steps = 64

lines = used_input.split("\n")
x_dim = len(lines[0])
y_dim = len(lines)


def move(position, displacement):
    x, y = position
    dx, dy = displacement
    new_x, new_y = x + dx, y + dy
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
current_positions = {starting_position}
for _ in range(steps):
    next_positions = set()
    for position in current_positions:
        next_positions = next_positions.union(step(position))
    current_positions = next_positions

print(len(current_positions))

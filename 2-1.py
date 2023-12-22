from aocd import get_data

data = get_data(day=2, year=2023)
example = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

used_input = data
lines = used_input.split("\n")
maxima = {
    "red": 12,
    "green": 13,
    "blue": 14
}
total = 0
for line in lines:
    game_no = int(line.split(":")[0].split(" ")[1])
    for handful in line.split(":")[1].split(";"):
        if any(int(cubes.strip().split(" ")[0]) > maxima.get(cubes.strip().split(" ")[1], 0) for cubes in handful.split(",")):
            break
    else:
        total += game_no

print(total)

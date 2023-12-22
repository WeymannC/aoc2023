from math import floor

from aocd import get_data

data = get_data(day=6, year=2023)
example = """Time:      7  15   30
Distance:  9  40  200"""
used_input = data

time_str, distance_str = used_input.split("\n")
times = [s for s in time_str.split(":")[1].strip().split(" ") if s != ""]
distances = [s for s in distance_str.split(":")[1].strip().split(" ") if s != ""]
time = int("".join(times))
distance = int("".join(distances))
solutions_float = (time**2-4*distance-0.1)**0.5
solution = floor(0.5*(time+solutions_float)) - floor(0.5*(time-solutions_float))

print(solution)

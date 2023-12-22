from aocd import get_data

data = get_data(day=4, year=2023)
example = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

used_input = data
lines = used_input.split("\n")

cards = {int(line.split(": ")[0].split(" ")[-1]): line for line in lines}

for line in lines:
    card_no = int(line.split(": ")[0].split(" ")[-1])
    card = line.split(": ")[1]
    number_strs = card.split(" | ")
    winning_numbers = {int(number) for number in number_strs[0].split(" ") if number != ""}
    own_numbers = {int(number) for number in number_strs[1].split(" ") if number != ""}
    if intersection := winning_numbers & own_numbers:
        lines.extend(cards[i] for i in range(card_no+1,card_no+1+len(intersection)))


print(len(lines))

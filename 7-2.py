import string
from collections import defaultdict, Counter
from functools import cmp_to_key
from math import floor

from aocd import get_data

data = get_data(day=7, year=2023)
example = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
used_input = data

card_values = {s: int(s) for s in string.digits}
card_values |= {"A": 14, "K": 13, "Q": 12, "J": 1, "T": 10}


def comp_hands(hand_a, hand_b):
    def comp_card_value(hand_string_a, hand_string_b):
        for a, b in zip(hand_string_a, hand_string_b):
            if card_values[a] < card_values[b]:
                return -1
            if card_values[a] > card_values[b]:
                return 1
        else:
            return 0

    hand_string_a = hand_a[0]
    hand_string_b = hand_b[0]
    counter_a = Counter(hand_string_a)
    counter_b = Counter(hand_string_b)
    sorted_counter_a = sorted(counter_a.items(), key=lambda x: x[1])
    sorted_counter_b = sorted(counter_b.items(), key=lambda x: x[1])
    if sorted_counter_a[-1][0] == "J":
        if len(sorted_counter_a) > 1:
            same_cards_a = sorted_counter_a[-1][1] + sorted_counter_a[-2][1]
        else:
            same_cards_a = 5
    else:
        same_cards_a = max(counter_a.values()) + counter_a["J"]
    if sorted_counter_b[-1][0] == "J":
        if len(sorted_counter_b) > 1:
            same_cards_b = sorted_counter_b[-1][1] + sorted_counter_b[-2][1]
        else:
            same_cards_b = 5
    else:
        same_cards_b = max(counter_b.values()) + counter_b["J"]
    if same_cards_a > same_cards_b:
        return 1
    if same_cards_a < same_cards_b:
        return -1
    if same_cards_a == 3:
        if sorted(counter_a.values())[-2] == 2 and sorted(counter_b.values())[-2] != 2:
            return 1
        if sorted(counter_a.values())[-2] != 2 and sorted(counter_b.values())[-2] == 2:
            return -1
    if same_cards_a == 2:
        if sorted(counter_a.values())[-2] == 2 and sorted(counter_b.values())[-2] != 2:
            return 1
        if sorted(counter_a.values())[-2] != 2 and sorted(counter_b.values())[-2] == 2:
            return -1
    return comp_card_value(hand_string_a, hand_string_b)


hand_key = cmp_to_key(comp_hands)
hands = [(hand.split(" ")[0], int(hand.split(" ")[1])) for hand in used_input.split("\n")]

total = 0
for rank, (hand, bid) in enumerate(sorted(hands, key=hand_key)):
    print(hand)
    total += (rank+1)*bid

print(total)

#!/usr/bin/env python3

from collections import Counter

def rule_of_double_part1(number):
    return max(Counter(number).values()) >= 2

def rule_of_double_part2(number):
    return Counter(Counter(number).values()).get(2, 0) >= 1

def is_valid_password(number):
    number = str(number)
    if rule_of_double_part1(number):
    # if rule_of_double_part2(number):
        # if list(number) == sorted(number):
        # if all(int(x) <= int(y) for x, y in zip(number, number[1:])):
        if all(x <= y for x, y in zip(number, number[1:])):  # even faster without `int`
            return True
    return False

if __name__ == "__main__":
    print(sum((is_valid_password(number) for number in range(372037, 905158))))

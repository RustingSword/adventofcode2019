#!/usr/bin/env python3

from collections import defaultdict
from math import ceil

import sys

material = defaultdict(list)  # [amount, (input, amount)]


def parse_amount_and_name(element):
    amount, name = element.split()
    return (int(amount), name)


def parse_input(filename):
    with open(filename) as fin:
        for line in fin:
            inputs, output = line.strip("\n").split("=>")
            out_amount, out_name = parse_amount_and_name(output)
            material[out_name].append(out_amount)
            for input_element in inputs.split(", "):
                in_amount, in_name = parse_amount_and_name(input_element)
                material[out_name].append((in_name, in_amount))


def analyze(target="FUEL", raw="ORE", amount=1):
    needed = defaultdict(int)
    needed[target] = amount
    left = defaultdict(int)
    while True:
        size = len(needed)
        if size == 1 and raw in needed:
            break
        keys = list(needed.keys())
        for current in keys:
            if current == raw:
                continue
            units = needed.pop(current)
            if current not in material:  # 'ORE'
                continue
            multiple = ceil((units - left[current]) / material[current][0])
            left[current] = multiple * material[current][0] - units
            for (input_element, input_amount) in material[current][1:]:
                needed[input_element] += multiple * input_amount - left[input_element]
                left[input_element] = 0
    return needed[raw]


def binary_search():
    low = 0
    high = 1000000000000
    limit = 1000000000000
    while low < high:
        mid = (low + high) // 2
        need = analyze(amount=mid)
        if need > limit:
            high = mid - 1
        elif need < limit:
            low = mid + 1
        else:
            return mid
    return low - 1


parse_input(sys.argv[1])
ore_for_1_fuel = analyze()
print(f"1 unit of FUEL needs {ore_for_1_fuel} units of ORE")
maximum = binary_search()
print(
    f"Given 1 trillion ORE, {maximum} amount of FUEL can be produced, "
    f"costing {analyze(amount=maximum)} units of ORE"
)

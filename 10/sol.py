#!/usr/bin/env python3

import sys
from collections import defaultdict, deque, namedtuple
from math import atan2, gcd, pi

import numpy as np

Coordinate = namedtuple("Coordinate", "x y")

data = open(sys.argv[1]).read().splitlines()
row, col = len(data), len(data[0])

asteroids = set(
    Coordinate(y, x) for x in range(row) for y in range(col) if data[x][y] == "#"
)

best = None
los = set()
for asteroid in asteroids:
    line_of_sight = defaultdict(list)
    for target in asteroids:
        if asteroid == target:
            continue
        x_diff, y_diff = asteroid.x - target.x, target.y - asteroid.y  # XXX
        if x_diff * y_diff == 0:
            diff = (np.sign(x_diff), np.sign(y_diff))
        else:
            divisor = gcd(x_diff, y_diff)
            diff = (x_diff // divisor, y_diff // divisor)
        line_of_sight[diff].append(target)
    if len(line_of_sight) > len(los):
        los = line_of_sight
        best = asteroid

print(len(los))  # part 1

########################################

sorted_angles = sorted(los, key=lambda x: (atan2(x[0], x[1]) + pi) % (pi * 2))

asteroids_in_line = [
    deque(sorted(los[angle], key=lambda x: (x.x - best.x) ** 2 + (x.y - best.y) ** 2))
    for angle in sorted_angles
]

seq = 0
while True:
    old_seq = seq
    for line in asteroids_in_line:
        if line:
            seq += 1
            asteroid = line.popleft()
            if seq == 200:
                print(asteroid)  # part 2
    if seq == old_seq:
        break

#!/usr/bin/env python3

import sys
from math import gcd
from math import atan2
from math import pi
from collections import namedtuple
from collections import defaultdict
from collections import deque

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
        if x_diff == 0:
            diff = (0, 1 if y_diff > 0 else -1)
        elif y_diff == 0:
            diff = (1 if x_diff > 0 else -1, 0)
        else:
            divisor = gcd(x_diff, y_diff)
            diff = (x_diff // divisor, y_diff // divisor)
        line_of_sight[diff].append(target)
    if len(line_of_sight) > len(los):
        los = line_of_sight
        best = asteroid

print(len(los))  # part 1

########################################

laser = best

# sort by angle
def _calc_angle(diff):
    radian = atan2(diff[0], diff[1])  # clockwise
    return (radian + pi) % (pi * 2)  # 0 - 2*pi


sorted_angles = sorted(los.keys(), key=lambda x: _calc_angle(x))

asteroids_in_line = []


def _dist_to_laser(p):
    x_diff = p.x - laser.x
    y_diff = p.y - laser.y
    return x_diff * x_diff + y_diff * y_diff


for angle in sorted_angles:
    asteroids_in_line.append(deque(sorted(los[angle], key=lambda x: _dist_to_laser(x))))

seq = 0
while True:
    old_seq = seq
    for line in asteroids_in_line:
        if line:
            seq += 1
            asteroid = line.popleft()
            if seq == 200:
                print(asteroid)
    if seq == old_seq:
        break

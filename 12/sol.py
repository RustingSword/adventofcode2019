#!/usr/bin/env python3.7

import re
import sys

from numpy import sign, lcm
from recordtype import recordtype
from collections import defaultdict
from loguru import logger

Moon = recordtype("Moon", "x y z vx vy vz")

Moon.__repr__ = lambda x: "{:3d} {:3d} {:3d} {:3d} {:3d} {:3d}".format(
    x.x, x.y, x.z, x.vx, x.vy, x.vz
)


def parse_input(inputfile):
    moons = []
    with open(inputfile) as fin:
        for line in fin:
            line = re.split("[=,]", line.strip("<>\n"))
            moons.append(Moon(int(line[1]), int(line[3]), int(line[5]), 0, 0, 0))
    return moons


def update_one_velocity(moon_a, moon_b):
    diff_x = sign(moon_b.x - moon_a.x)
    diff_y = sign(moon_b.y - moon_a.y)
    diff_z = sign(moon_b.z - moon_a.z)
    moon_a.vx += diff_x
    moon_a.vy += diff_y
    moon_a.vz += diff_z
    moon_b.vx -= diff_x
    moon_b.vy -= diff_y
    moon_b.vz -= diff_z


def update_velocity():
    for i in range(len(moons)):
        for j in range(i + 1, len(moons)):
            update_one_velocity(moons[i], moons[j])


def update_one_position(moon):
    moon.x += moon.vx
    moon.y += moon.vy
    moon.z += moon.vz


def update_position():
    for moon in moons:
        update_one_position(moon)


def calc_one_energy(moon):
    pot = abs(moon.x) + abs(moon.y) + abs(moon.z)
    kin = abs(moon.vx) + abs(moon.vy) + abs(moon.vz)
    return pot * kin


def calc_total_energy():
    return sum(calc_one_energy(moon) for moon in moons)


moons = parse_input(sys.argv[1])

axis_states = [defaultdict(list), defaultdict(list), defaultdict(list)]


def get_axis_state(axis, moon):
    if axis == 0:
        return (moon.x, moon.vx)
    if axis == 1:
        return (moon.y, moon.vy)
    if axis == 2:
        return (moon.z, moon.vz)


for i in range(len(moons)):
    moon = moons[i]
    for j in range(3):
        # pos, velocity
        state = get_axis_state(j, moon)
        axis_states[j][i] = state


def check_axis_repetition(axis):
    states = axis_states[axis]
    repeat = True
    for i in range(len(moons)):
        moon = moons[i]
        state = get_axis_state(axis, moon)
        if state != states[i]:
            repeat = False
    return repeat


step = 0
axis_steps = [sys.maxsize, sys.maxsize, sys.maxsize]
found = [False, False, False]
while True:
    update_velocity()
    update_position()
    step += 1
    if step == 1000:
        print(f"energy after 1000 steps: {calc_total_energy()}")
    for i in range(3):
        if check_axis_repetition(i):
            axis_steps[i] = min(step, axis_steps[i])
            found[i] = True
    if all(found):
        break

print(axis_steps, lcm.reduce(axis_steps))

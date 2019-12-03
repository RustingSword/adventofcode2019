#!/usr/bin/env python3
from collections import namedtuple

Point = namedtuple('Point', 'x y')
Line = namedtuple('Line', 'start end steps_before direction')

def scan(wires):
    x = y = steps = 0
    lines = []
    for p in wires:
        dist = int(p[1:])
        if p[0] == 'R':
            lines.append(Line(Point(x, y), Point(x + dist, y), steps, 1))
            x += dist
        elif p[0] == 'L':
            lines.append(Line(Point(x - dist, y), Point(x, y), steps, -1))
            x -= dist
        elif p[0] == 'U':
            lines.append(Line(Point(x, y), Point(x, y + dist), steps, 1))
            y += dist
        elif p[0] == 'D':
            lines.append(Line(Point(x, y - dist), Point(x, y), steps, -1))
            y -= dist
        else:
            raise ValueError('unknown direction {}'.format(p[0]))
        steps += dist
    return lines

def check_alignment(line):
    if line.start.x == line.end.x:
        return 'y'
    elif line.start.y == line.end.y:
        return 'x'
    raise ValueError('invalid line {}'.format(line))

def find_intersection(line1, line2, alignment):
    if alignment == 'y':
        line1, line2 = line2, line1
    if line2.start.y <= line1.start.y <= line2.end.y and \
            line1.start.x <= line2.start.x <= line1.end.x:
        inter_x = line2.start.x
        inter_y = line1.start.y
        w1_step = line1.steps_before
        w1_step += inter_x - line1.start.x if line1.direction == 1 else line1.end.x - inter_x
        w2_step = line2.steps_before
        w2_step += inter_y - line2.start.y if line2.direction == 1 else line2.end.y - inter_y
        return (inter_x, inter_y, w1_step + w2_step, line1, line2)
    return None


data = open('input').read().splitlines()
wire1 = data[0].split(',')
wire2 = data[1].split(',')

lines1 = scan(wire1)
lines2 = scan(wire2)

min_dist_from_origin = 1e10
min_steps = 1e10

for line1 in lines1:
    for line2 in lines2:
        alignment1 = check_alignment(line1)
        alignment2 = check_alignment(line2)
        if alignment1 == alignment2:
            continue
        inter = find_intersection(line1, line2, alignment1)
        if inter is not None:
            min_dist_from_origin = min(min_dist_from_origin, abs(inter[0]) + abs(inter[1]))
            min_steps = min(min_steps, inter[2])

print(min_dist_from_origin)  # part 1
print(min_steps)  # part 2


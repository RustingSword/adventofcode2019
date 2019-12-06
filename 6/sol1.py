#!/usr/bin/env python3
import sys
from collections import defaultdict
from collections import deque

orbit_relation = defaultdict(set)
with open(sys.argv[1]) as fin:
    for line in fin:
        center, obj = line.strip('\n').split(')')
        orbit_relation[center].add(obj)

orbit = deque()
orbit.append('COM')
depth = 0
num_orbits = 0
while orbit:
    size = len(orbit)
    for _ in range(size):
        current = orbit.popleft()
        orbit.extend(orbit_relation.get(current, []))
        num_orbits += depth
    depth += 1

print(num_orbits)

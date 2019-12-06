#!/usr/bin/env python3
import sys

orbit_map = dict(map(lambda x: x.split(')')[::-1], open(sys.argv[1]).read().splitlines()))

def find_route_to_com(obj):
    route = [obj]
    while orbit_map[obj] != 'COM':
        route.append(orbit_map[obj])
        obj = orbit_map[obj]
    return list(reversed(route + ['COM']))

route_of_you = find_route_to_com('YOU')
route_of_santa = find_route_to_com('SAN')

divergence = 0
while route_of_you[divergence] == route_of_santa[divergence]:
    divergence += 1
print('=>'.join(route_of_you))
print('=>'.join(route_of_santa))
print(f'divergence at {divergence} {route_of_you[divergence]}')
print(len(route_of_you) + len(route_of_santa) - 2 * divergence - 2)

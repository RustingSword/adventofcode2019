#!/usr/bin/env python3

import sys
from itertools import cycle

base = [0, 1, 0, -1]


def generate_pattern(phase):
    pattern = []
    for i in range(len(base)):
        pattern.extend([base[i]] * phase)
    shifted = pattern[1:] + [pattern[0]]
    return shifted


def fft(signal):
    size = len(signal)
    output = []
    for i in range(1, size+1):
        pattern = generate_pattern(i)
        res = 0
        for x, y in (
            zip(signal, pattern)
            if len(signal) <= len(pattern)
            else zip(signal, cycle(pattern))
        ):
            res += x * y
        output.append(int(str(res)[-1]))
    return output


data = list(map(int, open(sys.argv[1]).read().strip('\n')))

for i in range(100):
    data = fft(data)

print(''.join(map(str, data[:8])))

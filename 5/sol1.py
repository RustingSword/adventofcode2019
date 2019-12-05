#!/usr/bin/env python3

data = list(map(int, open('input').read().strip('\n').split(',')))
assert data[0] == 3
data[data[1]] = 1  # input ID 1


def _parse_code(code):
    code = str(code)
    code = '0' * (5 - len(code)) + code
    op = int(code[-2:])
    modes = list(reversed(code[:-2]))
    return op, modes


def _get_param(mode, index):
    assert mode in '01'
    return data[index] if mode == '1' else data[data[index]]


i = 2
while i < len(data):
    code = data[i]
    op, modes = _parse_code(code)
    if op == 1 or op == 2:
        first = _get_param(modes[0], i + 1)
        second = _get_param(modes[1], i + 2)
        outpos = data[i+3]
        data[outpos] = first + second if op == 1 else first * second
        i += 4
    elif op == 4:
        print(data[data[i+1]])
        i += 2
    else:
        assert op == 99
        break
